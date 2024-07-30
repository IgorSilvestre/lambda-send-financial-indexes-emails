mkdir -p package
cp lambda_function.py package/
cd package

# Install dependencies into the package directory
pip install -r ../requirements.txt -t .

# Create a zip file for the deployment package
zip -r ../lambda_function.zip .
cd ..
