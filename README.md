# Mayhem for API: Example CI integration

[![Mayhem for API](https://mayhem4api.forallsecure.com/static/media/logo.f8497128.svg)](http://mayhem4api.forallsecure.com/signup)

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

Want to try it? Start a [30-day free
trial](http://mayhem4api.forallsecure.com/signup).

## Example GitHub Actions Integration

This repo contains a simple python API that is being tested by Mayhem
for API.

### Starting a Mayhem for API scan in Github Actions

To scan your API with Mayhem for API in CI, you need to:
1) Download the Mayhem for API CLI
2) Start your API
3) Start the Mayhem for API scan

In GitHub actions, those steps translate to:

```yaml
    # Download Mayhem for API CLI for linux (also available for windows and Mac
    - name: Download API fuzzer CLI
      run: |
        curl -s -LO https://mayhem4api.forallsecure.com/downloads/cli/latest/linux-musl/mapi
        chmod +x ./mapi

    # Run API in test mode. We configured test mode to output stacktraces in
    # the error responses to improve the output of Mayhem for API.
    - name: Run API
      env:
        FASTAPI_ENV: test
      run: uvicorn src.main:app &

    # Run Mayhem for API
    - name: Mayhem for API Scan
      env:
        MAPI_TOKEN: ${{ secrets.MAPI_TOKEN }}
      run: ./mapi run fastapi 10 --url http://localhost:8000/ --sarif results.sarif --html results.html http://localhost:8000/openapi.json || true
```

This repo contains a [full example](.github/workflows/mapi.yml) for
reference.

## Results

Mayhem for API outputs reports in multiple formats (jUnit, SARIF, HTML).
In this instance, we requested a HTML report and a SARIF report.

### Artifact HTML Report

![HTML Report](https://mayhem4api.forallsecure.com/downloads/img/sample-report.png)

To artifact the report in your build, add this step to your pipeline:

```yaml
    # Archive HTML report
    - name: Archive code coverage results
      uses: actions/upload-artifact@v2
      with:
        name: mapi-report
        path: results.html
```

## Upload SARIF

![Mayhem for API issue in your
PR](http://mayhem4api.forallsecure.com/downloads/img/sarif-github.png)

Uploading SARIF to GitHub allows you to see any issue found by Mayhem
for API right on your PR! This currently requires you to have a GitHub
Enterprise Plan or have a public repository. To upload the SARIF report,
add this step to your pipeline:

```yaml
    # Upload SARIF file (only available on public repos or github enterprise)
    - name: Upload SARIF file
      uses: github/codeql-action/upload-sarif@v1
      with:
        sarif_file: results.sarif
```

If your API server sends back stacktraces in the 500 Internal Server
Error (only do this in a test environment -- never in production!),
Mayhem for API will try to map issues it finds to the exact line of code
that triggered the issue.
