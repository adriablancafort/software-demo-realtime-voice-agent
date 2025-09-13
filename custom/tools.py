from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.services.llm_service import FunctionCallParams


def get_tools_functions(browser):
    async def navigate_to(params: FunctionCallParams, page: str):
        """Navigate to a specific page in the application.
        
        Args:
            page: The page to navigate to.
        """

        ROUTES = {
            "home": 'a[href="/"]',
            "dashboard": 'a[href="/dashboard"]', 
            "analytics": 'a[href="/analytics"]',
            "team": 'a[href="/team"]',
            "settings": 'a[href="/settings"]',
        }
        
        try:
            selector = ROUTES[page.lower().strip()]
            await browser.click(selector)
            await params.result_callback({"message": f"Successfully navigated to {page} page."})
        except KeyError:
            await params.result_callback({"error": f"Unknown page '{page}'. Available pages: {list(ROUTES.keys())}"})
        except Exception as e:
            await params.result_callback({"error": f"Failed to navigate to {page}: {str(e)}"})


    async def type_into(params: FunctionCallParams, field: str, text: str):
        """Type text into a specific input field.
        
        Args:
            field: The field to type into.
            text: The text to type into the field.
        """

        FIELDS = {
            "settings_first_name": '#firstName',
            "settings_last_name": '#lastName', 
            "settings_email": '#email',
            "settings_bio": '#bio',
        }
        
        try:
            selector = FIELDS[field.lower().strip()]
            await browser.click(selector)
            await browser.type(selector, text)
            await params.result_callback({"message": f"Successfully typed '{text}' into {field} field."})
        except KeyError:
            await params.result_callback({"error": f"Unknown field '{field}'. Available fields: {list(FIELDS.keys())}"})
        except Exception as e:
            await params.result_callback({"error": f"Failed to type into {field}: {str(e)}"})


    async def click(params: FunctionCallParams, element: str):
        """Click on a specific element.
        
        Args:
            element: The element to click on.
        """

        ELEMENTS = {
            "settings_save_button": 'button:has-text("Save Changes")',
            "settings_email_notifications_toggle": 'button[role="switch"]:near(:text("Email Notifications"))',
            "settings_push_notifications_toggle": 'button[role="switch"]:near(:text("Push Notifications"))',
            "settings_marketing_emails_toggle": 'button[role="switch"]:near(:text("Marketing Emails"))',
            "analytics_export_report_button": 'button:has-text("Export Report")',
        }
        
        try:
            selector = ELEMENTS[element.lower().strip()]
            await browser.click(selector)
            await params.result_callback({"message": f"Successfully clicked on {element}."})
        except KeyError:
            await params.result_callback({"error": f"Unknown element '{element}'. Available elements: {list(ELEMENTS.keys())}"})
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
