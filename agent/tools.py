from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.services.llm_service import FunctionCallParams
from custom.selectors import NAVIGATE_ROUTES, TYPE_FIELDS, CLICK_ELEMENTS


def get_tools_functions(browser):
    async def navigate_to(params: FunctionCallParams, page: str):
        """Navigate to a specific page in the application.
        
        Args:
            page: The page to navigate to.
        """
        try:
            selector = NAVIGATE_ROUTES[page.lower().strip()]
            await browser.click(selector)
            await params.result_callback({"message": f"Successfully navigated to {page} page."})
        except KeyError:
            await params.result_callback({"error": f"Unknown page '{page}'. Available pages: {list(NAVIGATE_ROUTES.keys())}"})
        except Exception as e:
            await params.result_callback({"error": f"Failed to navigate to {page}: {str(e)}"})

    async def type_into(params: FunctionCallParams, field: str, text: str):
        """Type text into a specific input field.
        
        Args:
            field: The field to type into.
            text: The text to type into the field.
        """
        try:
            selector = TYPE_FIELDS[field.lower().strip()]
            await browser.click(selector)
            await browser.type(selector, text)
            await params.result_callback({"message": f"Successfully typed '{text}' into {field} field."})
        except KeyError:
            await params.result_callback({"error": f"Unknown field '{field}'. Available fields: {list(TYPE_FIELDS.keys())}"})
        except Exception as e:
            await params.result_callback({"error": f"Failed to type into {field}: {str(e)}"})

    async def click(params: FunctionCallParams, element: str):
        """Click on a specific element.
        
        Args:
            element: The element to click on.
        """
        try:
            selector = CLICK_ELEMENTS[element.lower().strip()]
            await browser.click(selector)
            await params.result_callback({"message": f"Successfully clicked on {element}."})
        except KeyError:
            await params.result_callback({"error": f"Unknown element '{element}'. Available elements: {list(CLICK_ELEMENTS.keys())}"})
        except Exception as e:
            await params.result_callback({"error": f"Failed to click on {element}: {str(e)}"})

    async def scroll_page(params: FunctionCallParams, direction: str, amount: int = 500):
        """Scroll the page up or down.
        
        Args:
            direction: Direction to scroll. Must be either "up" or "down".
            amount: Amount to scroll in pixels.
        """
        y = amount if direction == "down" else -amount
        await browser.scroll(0, y)
        await params.result_callback({"message": "Scrolled " + direction})

    return [
        navigate_to,
        type_into,
        click,
        scroll_page,
    ]


def get_tools_schema(browser) -> ToolsSchema:
    """Create ToolsSchema"""
    tools_functions = get_tools_functions(browser)
    return ToolsSchema(standard_tools=tools_functions)
