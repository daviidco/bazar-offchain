html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style type="text/css">
        body {{
            font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
            color: #414c5b;
            width: 626px;
        }}
    </style>
</head>
<body>
    <div style="text-align: left;">
        <header>
            <img src="https://s3-offchain-test.s3.us-east-2.amazonaws.com/email_images/assets/group-12796.png" alt="">
        </header>
        <section style="padding-left: 65px; padding-right: 65px; margin-top: 31px; margin-bottom: 41px;">
            <p>
                Hi <strong>admin</strong>, this user needs to review the documents for profile approval, once the documents are reviewed please login to
                the platform to validate or reject the user.
            </p>
            <p>
                <h2>{company_name}</h2>
                <p>{rol}</p>
                <div style="font-size: 20.2px; font-weight: 600; font-stretch: normal; font-style: normal;">
                    Company documents
                </div>
                <p>Go to the link to review the folder with the documents. {link}</p>
            </p>
        </section>
        <footer style="font-size: 11.7px; text-align: center;">
            <p>
                Copyright © 2022
            </p>
        </footer>
    </div>
</body>
</html>
'''
