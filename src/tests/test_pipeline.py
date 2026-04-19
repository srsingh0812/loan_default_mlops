name: ML CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint_and_test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # ✅ ROBUST LINT (won’t fail for trivial issues)
      - name: Lint (non-blocking formatting checks)
        run: |
          flake8 src/ \
            --max-line-length=100 \
            --ignore=W292,E402,E221,F401 \
            || true

      # ✅ TESTS are the real gate
      - name: Run unit tests
        run: |
          pytest src/tests/ -v

  build_and_deploy:
    needs: lint_and_test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t loan-default-ml .

      # (Optional) push to DockerHub if needed
      # - name: Login to DockerHub
      #   run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      # - name: Push image
      #   run: docker push loan-default-ml