To build and deploy your Django app to Azure Container Apps, follow these steps:

1. **Build the Docker Image:**
   Navigate to the root directory of your project and build the Docker image using the `Dockerfile`.

   ```bash
   docker build -t mspr_covid_ekym:latest .
   ```

2. **Run the Docker Container Locally (Optional):**
   Test the Docker image locally to ensure it works as expected.

   ```bash
   docker run -p 8000:8000 mspr_covid_ekym:latest
   ```

3. **Push the Docker Image to a Container Registry:**
   Tag the Docker image and push it to a container registry like Docker Hub or Azure Container Registry (ACR).

   ```bash
   # Tag the image
   docker tag mspr_covid_ekym:latest killianfvt/mspr_covid_ekym:latest

   # Push the image
   docker push killianfvt/mspr_covid_ekym:latest
   ```

4. **Create an Azure Container App:**
   Use the Azure CLI to create a new Azure Container App.

   ```bash
   az containerapp create --name your-container-app --resource-group your-resource-group --image your_registry/your_django_app:latest --environment your-environment --ingress external --target-port 8000
   ```

5. **Configure Environment Variables:**
   Set the necessary environment variables for your Django app, such as database credentials.

   ```bash
   az containerapp envvar set --name your-container-app --resource-group your-resource-group --env-vars DB_USER=ekym DB_PWD=1E2k3Y4m_
   ```

6. **Deploy the Container App:**
   The container app should now be deployed and running. You can check the status and get the URL to access your app.

   ```bash
   az containerapp show --name your-container-app --resource-group your-resource-group --query properties.configuration.ingress.fqdn
   ```

These steps will help you build, push, and deploy your Django app to Azure Container Apps.