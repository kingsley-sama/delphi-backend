def verification_email_template(user_name: str, verify_link: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Verify Email</title>

            <style>
            body {{
                margin: 0;
                padding: 0;
                background: #f5f5f5;
                font-family: Arial, Helvetica, sans-serif;
            }}

            .wrapper {{
                padding: 40px 16px;
            }}

            .card {{
                max-width: 520px;
                margin: 0 auto;
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
                padding: 40px 32px;
                text-align: center;
            }}

            .icon {{
                width: 56px;
                height: 56px;
                margin: 0 auto;
                border-radius: 999px;
                background: #eef2ff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            }}

            .brand {{
                margin-top: 24px;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: #4f46e5;
            }}

            .title {{
                margin-top: 16px;
                font-size: 24px;
                font-weight: 600;
                color: #111827;
                line-height: 1.4;
            }}

            .primary {{
                color: #4f46e5;
            }}

            .accent {{
                color: #ec4899;
            }}

            .message {{
                margin-top: 16px;
                font-size: 14px;
                line-height: 1.7;
                color: #6b7280;
            }}

            .button {{
                display: inline-block;
                margin-top: 32px;
                padding: 14px 32px;
                background: #4f46e5;
                color: white !important;
                text-decoration: none;
                border-radius: 999px;
                font-size: 14px;
                font-weight: bold;
            }}

            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e5e5e5;
                font-size: 11px;
                line-height: 1.6;
                color: #9ca3af;
            }}
            </style>
            </head>

            <body>
                <div class="wrapper">
                <div class="card">
                    <div class="icon">✉️</div>

                    <p class="brand">Exposeprofi · Revision</p>

                    <h1 class="title">
                    Hi <span class="primary">{user_name}</span>, confirm your
                    <span class="accent">email</span>
                    </h1>

                    <p class="message">
                    Click the button below to verify your email address. This link expires
                    in 15 minutes.
                    </p>

                    <a
                    class="button"
                    href="{verify_link}"
                    >
                    Verify Email
                    </a>

                    <p class="footer">
                    You're receiving this email because someone signed up on Revision
                    using this address. If this wasn't you, you can safely ignore this
                    message.
                    </p>
                </div>
                </div>
            </body>
        </html>
    """
