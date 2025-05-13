
# import yagmail

# def send_alert(subject, body, image_path=None, to_email='your_email@example.com'):
#     try:
#         yag = yagmail.SMTP('your_email@example.com', 'your_app_password')
#         contents = [body]
#         if image_path:
#             contents.append(image_path)
#         yag.send(to=to_email, subject=subject, contents=contents)
#     except Exception as e:
#         print(f"Email error: {e}")
