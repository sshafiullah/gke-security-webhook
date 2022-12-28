# gke-security-webhook
This repo contains a Mutating Webhook app that automatically inserts pod security policies for new namespaces. 
This app was tested against GKE version 1.23 and GCP Cloud Function version 1, but can easily be adapated for use on AWS Lambda.

# Requirements
1) GKE cluster version 1.23+
2) GCP Cloud Function access.The cloud function created must be publicly available with the cloudfunctions.invoker role. 
   You can assign this permission from the GCP console or by running command:
   gcloud functions add-iam-policy-binding <FUNCTION NAME> --member="allUsers" --role="roles/cloudfunctions.invoker" --region=<REGION>
3) (Optional): If you would like to create a GitOps flow to automate any change deployments, you will need to create a Cloud Build job using the supplied cloudbuild.yaml file. 

# How it works

The main.py app file is meant to be deployed on a gen 1 or 2 Cloud Function. The cfmutate.yaml file is meant to be deployed on your local GKE cluster
Once the cloud function has been deployed with the appropriate service account permissions and invoker permissions, copy the public URL for the function and add it to the cfmutate.yaml file in the 'url' option.

Deploy cfmutate.yaml to one or more GKE clusters and any new namespace that gets created on these clusters will automatically be patched with the Pod Security Standard policy of *Baseline*

# How to Setup a GitOps Flow 

You can optionally create a GitOps flow to automatically pick up any changes to this repo or a cloned repo. GCP Cloud Build can be used with the supplied cloudbuild.yaml file to achieve this. You will however need to create a service account with the following permissions:

   - Cloud Build Service Account
   - Cloud Function Developer
   - Service Account User
   
Create a trigger event for the Cloud Build job and point it to this repo or a cloned private copy of this repo. 

# References:
Visit my blog for a detailed overview of why and how this project was created: 
https://sshafiullah.wixsite.com/blog/post/applying-pod-security-admissions-policies-on-gke-clusters
https://sshafiullah.wixsite.com/blog/post/kubernetes-webhooks
