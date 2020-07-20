#!/bin/bash
cd $(dirname $0)
gcloud functions deploy million_celebration_upload --entry-point main_upload --runtime python37 --trigger-http --memory 2048MB --timeout 500s --ingress-settings internal-only --allow-unauthenticated
gcloud functions deploy million_celebration_tweet --entry-point main_tweet --runtime python37 --trigger-http --memory 2048MB --timeout 500s --ingress-settings internal-only --allow-unauthenticated
