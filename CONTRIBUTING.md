# Contributing to kernpy

>
> Go to [Developer Notes](#developer-notes) for specific guidelines for developers.
> 

We welcome your contributions to `kernpy`‼️  
Our goal is to make contributing as easy and transparent as possible. Whether you're fixing bugs, improving documentation, or adding new features, or creating new tests, thank you for helping improve `kernpy`!

<br>

## Step-by-Step Guide 📖
1. Fork the Repository
- **Fork the repo:** Start by forking the kernpy repository to your GitHub account.
- **Clone your fork:** Clone your fork locally.
- **Create a branch:** Always create your branch from `main` for any changes:
```bash
git checkout -b <your-feature-name>
```

2. Make Your Changes 🔧
   Develop your feature or fix: Write your code and include tests for any new functionality. If you're fixing a bug or adding a new feature, please include a test that demonstrates the issue.
   Build and run tests: Ensure that your changes pass all tests. Run:
   
```bash
python3 -m pip install -r requirements.txt
cd tests && python -m pytest
```

3. Create a Pull Request (PR) 📬
   Commit your changes: Use clear and descriptive commit messages.
   Push your branch: Push your branch to your fork:
   git push origin feature/your-feature-name
   Open a PR: Open a pull request from your branch in your fork to the main branch of the kernpy repository. Provide a detailed description of your changes, reference any related issues, and feel free to thank the community for their support! 😊

4. Issues and Feedback 🗣️
   Report issues: If you find a bug or have a feature request, please open an issue with clear steps to reproduce the problem.
   Engage with the community: Discuss ideas and ask for clarifications by commenting on issues. We’re open and collaborative!

### Additional Guidelines 

Documentation: Update or add documentation as needed, including usage examples or API changes.
Acknowledgments: We appreciate every contribution. A huge thank you to all contributors! 🙏
Testing: Every change must pass the build tests. Run tests locally using the provided script to confirm that your changes do not break the build.


### License

By contributing to `kernpy`, you agree that your contributions will be licensed under the terms specified in the LICENSE file at the root of this project.

Happy coding and thank you for contributing! 🚀


# Developer notes

> [!IMPORTANT]
> - Add the development dependencies to the `requirements.txt` file.
> - Add the production dependencies to the `pyproject.toml` file.
> - After every change in the grammar, the next steps are mandatory:
> - - Run the `antlr4.sh` script (JAVA required).
> - - Commit & push the changes to the repository.


- Generate antrl4 grammar:
- For generating the Python code required for parsing the **kern files, the shell script `antlr4.sh` inside the `kernpy` package must be run.

```shell
./antlr4.sh
```

Install all the dependencies using the `requirements.txt` file:
```shell
pip install -r requirements.txt
```

Otherwise, install the required packages manually:


- It requires the `antlr4` package to be installed using:
```shell
pip install antlr4-python3-runtime
```


- For visualizing the bounding boxes, the library, the `Pillow` library is required:
```shell
pip install Pillow
```

- To parse a IIIF (International Image Interoperability Framework) manifest in Python, we use the `requests` library to fetch the manifest file:
```shell
pip install requests
```

- If fetching data from `https` fails, install the following version of `urllib`:
```shell
pip install urllib3==1.26.6
```

It has been tested with version 4.13.1 of the package.

