from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html>
<head><title>Test PDF</title></head>
<body>
  <h1>Hello from WeasyPrint</h1>
  <p>This is a test PDF generated with WeasyPrint.</p>
</body>
</html>
"""

HTML(string=html_content).write_pdf("test_output.pdf")
print("✅ PDF generated successfully.")
