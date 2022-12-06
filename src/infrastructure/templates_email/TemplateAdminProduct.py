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
            <img src="https://s3-offchain-test.s3.us-east-2.amazonaws.com/email_images/assets/group-12797.png" alt="">
        </header>
        <section style="padding-left: 65px; padding-right: 65px; margin-top: 31px; margin-bottom: 41px;">
            <p>
                Hi <strong>admin</strong>, this user needs to review the documents for product approval, once the documents are reviewed please login to the
                platform to validate or reject the product.
            </p>
            <p>
            <div>
                <div style="float: left; margin-right: 1%;">
                    <img src="./assets/coffebeans.png" alt="">
                </div>
                <div style="color: #023047">
                    <h2>{product_name}</h2>
                </div>
            </div>
            <div>{user_name} <span style="margin: 2px 14px 2px 15px; color: #cbd5e1;">|</span> {company_name}</div>
            <div style="font-size: 20.2px; font-weight: 600; font-stretch: normal; font-style: normal; color: #023047; margin-top: 25.3px;">
                Product documents
            </div>
            <p>Go to the link to review the folder with the documents. <a href="{link}">{link}</a> </p>
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