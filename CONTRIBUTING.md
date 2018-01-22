# Contributing

## Pull Request Submission Guidelines

Before you submit your pull request consider the following guidelines: 
* Please communicate with us up front about any new feature you would like to add, to avoid disappointment later. You can do this by creating an [issue](https://github.com/eEcoLiDAR/eEcoLiDAR/issues).
* Fork the repository to your own git account if you don't have write access
* Make your changes in a new git branch:
`git checkout -b my-fix-branch master`
* Install the development environment
`python setup.py develop`
* Make your changes and add tests demonstrating that you fixed the bug or covering the new feature you added
* Order your imports
`isort your_changed_file.py`
* Format your code according the the project standard
`yapf -i your_changed_file.py`
* Check that your code is clean and fix style or other issues
`prospector`
* Run tests and make sure they pass
`python setup.py test`
* Commit your changes and upload
`git add changed_file_1.py changed_file_2.py`
`git commit -m 'Your commit message'`
`git push`
* Create a [pull request](https://github.com/eEcoLiDAR/eEcoLiDAR/pulls)
