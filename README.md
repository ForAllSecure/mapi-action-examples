# Mayhem for API: Example CI integration

[![Mayhem for API](https://mayhem4api.forallsecure.com/api/v1/api-target/forallsecure/forallsecure-mapi-action-examples/badge/icon.svg?scm_branch=main)](https://mayhem4api.forallsecure.com/forallsecure/forallsecure-mapi-action-examples/latest-job?scm_branch=main)

[![Mayhem for API](https://mayhem4api.forallsecure.com/downloads/img/mapi-logo-full-color.svg)](http://mayhem4api.forallsecure.com/signup)

## About Mayhem for API

🧪 Modern App Testing: Mayhem for API is a dynamic testing tool that
catches reliability, performance and security bugs before they hit
production.

🧑‍💻 For Developers, by developers: The engineers building
software are the best equipped to fix bugs, including security bugs. As
engineers ourselves, we're building tools that we wish existed to make
our job easier! 

🤖 Simple to Automate in CI: Tests belong in CI, running on every commit
and PRs. We make it easy, and provide results right in your PRs where
you want them. Adding Mayhem for API to a DevOps pipeline is easy.

Want to try it? [Sign up for free](https://app.mayhem.security)!

## Example GitHub Actions Integration

This repo contains a simple python API that is being tested by Mayhem
for API.

### Starting a Mayhem for API scan in Github Actions

To scan your API with Mayhem for API in CI, you need to:
1) Start your API
2) Start the Mayhem for API scan

In GitHub actions, those steps translate to:

```yaml
    # Run API in test mode. We configured test mode to output stacktraces in
    # the error responses to improve the output of Mayhem for API.
    - name: Run API
      env:
        FASTAPI_ENV: test
      run: uvicorn src.main:app &

    # Run Mayhem for API
    - name: Run Mayhem for API to check for vulnerabilities
      uses: ForAllSecure/mapi-action@v2
      with:
        mayhem-token: ${{ secrets.MAYHEM_TOKEN }}
        api-url: http://localhost:8000
        api-spec: http://localhost:8000/openapi.json
```

This repo contains a [full example](.github/workflows/mapi.yml) for
reference.

# Reports

Mayhem for API generate reports when you pass `sarif-report` or
`html-report` to the input. Make sure to pass `continue-on-error` to the
Mayhem for API step if you want to process the reports in follow-up
steps.

## Artifact HTML Report

![HTML Report](https://mayhem4api.forallsecure.com/downloads/img/sample-report.png)

To artifact the report in your build, add this step to your pipeline:

```yaml
- name: Run Mayhem for API to check for vulnerabilities
  uses: ForAllSecure/mapi-action@v2
  continue-on-error: true
  with:
    mayhem-token: ${{ secrets.MAYHEM_TOKEN }}
    api-url: http://localhost:8000 # <- update this
    api-spec: your-openapi-spec-or-postman-collection.json # <- update this
    html-report: mapi.html

# Archive HTML report
- name: Archive Mayhem for API report
  uses: actions/upload-artifact@v3
  with:
    name: mapi-report
    path: mapi.html
```

## GitHub Code Scanning support

![Mayhem for API issue in your
PR](http://mayhem4api.forallsecure.com/downloads/img/sarif-github.png)

Uploading SARIF reports to GitHub allows you to see any issue found by
Mayhem for API right on your PR, as well as in the "Security" tab of
your repository. This currently requires you to have a GitHub Enterprise
Plan or have a public repository. To upload the SARIF report, add this
step to your pipeline:

```yaml
- name: Run Mayhem for API to check for vulnerabilities
  uses: ForAllSecure/mapi-action@v2
  continue-on-error: true
  with:
    mayhem-token: ${{ secrets.MAYHEM_TOKEN }}
    api-url: http://localhost:8000 # <- update this
    api-spec: your-openapi-spec-or-postman-collection.json # <- update this
    sarif-report: mapi.sarif

# Upload SARIF file (only available on public repos or github enterprise)
- name: Upload SARIF file
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: mapi.sarif
```

If your API server sends back stacktraces in the 500 Internal Server
Error (only do this in a test environment -- never in production!),
Mayhem for API will try to map issues it finds to the exact line of code
that triggered the issue.
