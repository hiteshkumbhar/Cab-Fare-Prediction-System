# Car Fare Price Prediction

## Overview
This project is a car fare price prediction system that leverages AWS cloud services for data processing, model training, and deployment. The prediction is based on two major factors: **distance** and **time**, which are acquired using the **TomTom API**.

## Tech Stack
- **AWS S3** - Data storage
- **AWS Glue (PySpark)** - ETL processing
- **AWS SageMaker** - Model training and deployment
- **EC2** - Hosting the deployed model
- **Power-BI** - For Dashboarding & Reporting 
- **Streamlit** - Web application for predictions
- **TomTom API** - Fetching distance and time for fare calculations

## Project Workflow
1. **Data Collection**: Data is sourced from a structured dataset and enriched using TomTom API for real-time distance and time estimates.
2. **ETL Process**:
   - Data is ingested into AWS S3.
   - AWS Glue (PySpark) processes and cleans the data  through ETL pipeline .
3. **Model Training**:
   - The processed data is used to train a machine learning model in AWS SageMaker.
   - The trained model is deployed on an EC2 instance and as a pickel file .
4. **Prediction Service**:
   - A Streamlit web application is developed for users to input pickup and drop-off locations.
   - The app fetches distance and time (trip duration )from the TomTom API and makes predictions using the deployed model.

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/car-fare-prediction.git
   cd car-fare-prediction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit_app run main.py
   ```

## Deployment on AWS
- **Data Storage:** Raw and processed data stored in AWS S3.
- **ETL Pipeline:** AWS Glue processes data and loads it for training.
- **Model Training & Deployment:** Model is trained in SageMaker and deployed on EC2.
- **Web Application:** Streamlit app hosted for real-time predictions.

## Future Enhancements
- Integrate more features like weather and traffic conditions.
- Integrate kafka for user inputs 
- Optimize the ML model for better accuracy.
- Implement containerization using Docker for easier deployment.

## Deployed Link and Repo
used for trying streamlit cloud for free  deployement & hosting 
aws deployement deleted after deployement 
https://github.com/rishikeshdound/cloud_Deploy
app deployed might be taken down : https://rishi-cabfare.streamlit.app/ 

## Author
[Rishikesh Dound](https://github.com/rishikeshdound)

## License
This project is licensed under the MIT License.

