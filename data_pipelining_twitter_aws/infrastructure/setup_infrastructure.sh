display_usage()
{
echo "Usage:$0 [StackName]"
}
if [[ $# -lt 1 ]];then
	display_usage
	exit 1
fi

BucketName="info7374_data_pipelining.${2}"

StackID=$(aws cloudformation create-stack --stack-name $1 --template-body file://twitter_analytics.json --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=S3Bucket,ParameterValue="${BucketName}"  |grep StackId)
if [[ $? -eq 0 ]]; then
    stackCompletion=$(aws cloudformation wait stack-create-complete --stack-name "$1")
        if [ $? -eq 0 ]; then
            echo "Stack with name $1 creation completed successfully!!"
            exit 0
        else
            echo "Error in creating CloudFormation Stack"
        fi
else
    echo "Error in creating CloudFormation Stack"
    echo $StackID
    exit 1
fi