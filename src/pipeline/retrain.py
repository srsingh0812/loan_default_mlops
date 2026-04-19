import subprocess
import logging

logger = logging.getLogger(__name__)

def trigger_retraining() -> None:
    """
    Simple retraining trigger.
    In prod, this could call a job queue or CI workflow.
    """
    logger.info("Triggering retraining pipeline...")

    result = subprocess.run(
        ["python", "src/models/train.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        logger.info("Retraining completed successfully")
    else:
        logger.error("Retraining failed")
        logger.error(result.stderr)