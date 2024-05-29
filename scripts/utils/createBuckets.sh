#!/bin/bash
# BUCKET_LIST=("sure-app1-static-files" "sure-app2-static-files")

function createBuckets() {
  local bucket_list

  bucket_list=("$@")
  for bucket in "${bucket_list[@]}"; do
    echo "Creating bucket: $bucket"
    awslocal s3api create-bucket --bucket "$bucket"
    echo "Creating bucket objects for bucket: $bucket"
    createBucketObjects "$bucket"
  done
}

function createBucketObjects() {
  local bucket

  bucket=$1
  awslocal s3api put-object --bucket "$bucket" --key deploy1/index.html
  awslocal s3api put-object --bucket "$bucket" --key deploy1/css/font.css
  awslocal s3api put-object --bucket "$bucket" --key deploy1/images/hey.png

  awslocal s3api put-object --bucket "$bucket" --key deploy2/root.html
  awslocal s3api put-object --bucket "$bucket" --key deploy2/styles/font.css
  awslocal s3api put-object --bucket "$bucket" --key deploy2/img/hey.png

  awslocal s3api put-object --bucket "$bucket" --key deploy3/base.html
  awslocal s3api put-object --bucket "$bucket" --key deploy3/fonts/font.css
  awslocal s3api put-object --bucket "$bucket" --key deploy3/png/hey.png
}

function setupS3() {
  local bucket_list

  bucket_list=("$@")

  createBuckets "${bucket_list[@]}"
}