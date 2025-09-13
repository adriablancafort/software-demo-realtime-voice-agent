NAVIGATE_ROUTES = {
    "home": 'a[href="/"]',
    "dashboard": 'a[href="/dashboard"]',
    "analytics": 'a[href="/analytics"]',
    "team": 'a[href="/team"]',
    "settings": 'a[href="/settings"]',
}

TYPE_FIELDS = {
    "settings_first_name": '#firstName',
    "settings_last_name": '#lastName',
    "settings_email": '#email',
    "settings_bio": '#bio',
}

CLICK_ELEMENTS = {
    "settings_save_button": 'button:has-text("Save Changes")',
    "settings_email_notifications_toggle": 'button[role="switch"]:right-of(:text("Email Notifications"))',
    "settings_push_notifications_toggle": 'button[role="switch"]:right-of(:text("Push Notifications"))',
    "settings_marketing_emails_toggle": 'button[role="switch"]:right-of(:text("Marketing Emails"))',
    "analytics_export_report_button": 'button:has-text("Export Report")',
}