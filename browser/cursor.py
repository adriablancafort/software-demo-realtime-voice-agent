import asyncio

async def inject_cursor(page, transition_duration=0.3):
    CURSOR_JS = f"""
    if (!window.cursor) {{
        const cursor = document.createElement('div');
        cursor.style.position = 'fixed';
        cursor.style.width = '24px';
        cursor.style.height = '24px';
        cursor.style.background = 'rgba(255, 0, 0, 0.8)';
        cursor.style.border = '2px solid #ff0000';
        cursor.style.borderRadius = '50%';
        cursor.style.zIndex = '2147483647';
        cursor.style.pointerEvents = 'none';
        cursor.style.left = 'calc(50vw - 12px)';
        cursor.style.top = 'calc(50vh - 12px)';
        cursor.style.transition = 'left {transition_duration}s cubic-bezier(.25,1,.5,1), top {transition_duration}s cubic-bezier(.25,1,.5,1)';
        cursor.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.5)';
        document.body.appendChild(cursor);
        window.cursor = cursor;
    }}
    """
    await page.evaluate(CURSOR_JS)


async def click_element(page, x, y, transition_duration=0.3, click_duration=0.2):
    CLICK_JS = f"""
    if (window.cursor) {{
        window.cursor.style.left = '{x-12}px';
        window.cursor.style.top = '{y-12}px';

        const onTransitionEnd = () => {{
            window.cursor.removeEventListener('transitionend', onTransitionEnd);

            window.cursor.animate([
                {{ transform: 'scale(1)', opacity: 1 }},
                {{ transform: 'scale(0.85)', opacity: 0.8 }},
                {{ transform: 'scale(1)', opacity: 1 }}
            ], {{
                duration: {click_duration * 1000},
                easing: 'ease-out'
            }});
        }};
        window.cursor.addEventListener('transitionend', onTransitionEnd, {{ once: true }});
    }}
    """
    await page.evaluate(CLICK_JS)
    await asyncio.sleep(transition_duration)
