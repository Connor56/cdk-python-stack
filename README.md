# Welcome to the Simplest Python Lambda Stack!

This is a basic project for CDK development with Python. It includes a single Python Lambda function, in a basic stack.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up with Poetry environment management to simplify dependencies. You can set the project up with:

```bash
poetry install --no-root
```

Then activate the project's environment with:

```bash
poetry shell
```

## Deploying the stack

To deploy the stack, run:

```bash
cdk deploy
```

You check it worked by taking the output URL and running:

```bash
curl <output-url>
```

## Destroying the stack

To destroy the stack, run:

```bash
cdk destroy
```

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

Enjoy!
