# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

#
# This file contains a template email
# @author David Córdoba
#
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
            <img src="https://s3-offchain-test.s3.us-east-2.amazonaws.com/email_images/assets/group-12797-2.png" alt="">
        </header>
        <section style="padding-left: 65px; padding-right: 65px; margin-top: 31px; margin-bottom: 41px;">
            <p>
                We are sorry <strong>{user_name}</strong>, the Bazar team has rejected your product, please review the comments and contact our support team, we
                apologize for the inconvenience
            </p>
            <p>
            <div style="justify-content: center; align-items: center; text-align: center;">
                <div style="color: #023047">
                    <h3><span style="margin-right: 1%;"><img src="https://s3-offchain-test.s3.us-east-2.amazonaws.com/email_images/assets/leaft.png"></span>Your product was rejected<span style="margin-left: 2%"><img src="https://s3-offchain-test.s3.us-east-2.amazonaws.com/email_images/assets/close-circle.png"></span></h3>
                </div>
                <div style="text-align: left; margin-left: 20%; margin-right: 20%;">
                    <h4>Comments:</h4>
                    <p>{comment}</p>
                </div>
            </div>
            </p>
            <br>
            <p style="text-align: center;">
                <a style="padding: 14px 50px; border-radius: 8px; background-color: #054f6e; color: #fff; text-decoration: none; "
                    href="{link_bazar}">Go to bazar</a>
            </p>
        </section>
        <footer style="font-size: 11.7px; text-align: center;">
            <p>
                Copyright © 2023
            </p>
        </footer>
    </div>
</body>

</html>
'''
