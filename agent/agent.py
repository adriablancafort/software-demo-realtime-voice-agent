import os
from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.runner.types import RunnerArguments
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport

from browser.browser import WebBrowser
from agent.tools import get_tools_schema, get_tools_functions
from custom.prompts import initial_url, system_prompt, connection_prompt


load_dotenv()


async def agent(transport: BaseTransport):
    browser = WebBrowser()
    await browser.initialize()
    
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))
    
    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="6f84f4b8-58a2-430c-8c79-688dad597532",
        model="sonic-2",
        params=CartesiaTTSService.InputParams(
            speed="fast"
        )
    )
    
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1",
        run_in_parallel=False
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    tools_schema = get_tools_schema(browser)
    context = OpenAILLMContext(messages, tools=tools_schema)
    context_aggregator = llm.create_context_aggregator(context)
    
    pipeline = Pipeline([
        transport.input(),
        stt,
        context_aggregator.user(),
        llm,
        tts,
        transport.output(),
        context_aggregator.assistant(),
    ])
    
    task = PipelineTask(pipeline, params=PipelineParams())
    
    for tools_function in get_tools_functions(browser):
        llm.register_direct_function(tools_function)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        await browser.goto(initial_url)
        messages.append({"role": "system", "content": connection_prompt})
        await task.queue_frames([LLMRunFrame()])
    
    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        await browser.close()
        await task.cancel()
    
    runner = PipelineRunner()
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    transport = SmallWebRTCTransport(
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        ),
        webrtc_connection=runner_args.webrtc_connection,
    )

    await agent(transport)
