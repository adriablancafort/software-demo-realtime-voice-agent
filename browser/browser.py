import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from browser.cursor import inject_cursor, click_element


class WebBrowser:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
    
    async def initialize(self):
        """Initialize the browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
    
    async def goto(self, url: str):
        """Navigate to a URL"""
        await self.page.goto(url)
        await inject_cursor(self.page)
    
    async def click(self, selector: str):
        """Click on an element given a CSS selector"""
        element = await self.page.query_selector(selector)
        if element:
            box = await element.bounding_box()
            if box:
                await click_element(self.page, box['x'] + box['width']/2, box['y'] + box['height']/2)
            await element.click()
        else:
            raise Exception(f"Element not found: {selector}")
    
    async def type(self, selector: str, text: str, delay: float = 0.015):
        """Type text into an input field"""
        element = await self.page.query_selector(selector)
        if element:
            await element.fill("")
            for char in text:
                await element.type(char, delay=int(delay * 1000))
        else:
            raise Exception(f"Element not found: {selector}")
    
    async def scroll(self, x: int, y: int):
        """Scroll the page given coordinates"""
        await self.page.evaluate(f"window.scrollBy({{ top: {y}, left: {x}, behavior: 'smooth' }});")
        await asyncio.sleep((abs(max(x, y))) / 1000 + 0.3)
    
    async def close(self):
        """Close the browser"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
