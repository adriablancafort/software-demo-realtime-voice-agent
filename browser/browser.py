from playwright.async_api import async_playwright, Page, Browser, BrowserContext


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
        return f"Navigated to {url}"
    
    async def click(self, selector: str):
        """Click on an element given a CSS selector"""
        await self.page.click(selector)
        return f"Clicked on element: {selector}"
    
    async def type(self, selector: str, text: str):
        """Type text into an input field"""
        await self.page.fill(selector, text)
        return f"Typed '{text}' into {selector}"
    
    async def scroll(self, x: int, y: int):
        """Scroll the page given coordinates"""
        await self.page.evaluate(f"window.scrollBy({x}, {y})")
        return f"Scrolled by x:{x}, y:{y}"
    
    async def close(self):
        """Close the browser"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
