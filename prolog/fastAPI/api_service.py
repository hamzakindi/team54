from fastapi import FastAPI, HTTPException
from pyswip import Prolog
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

def init_prolog():
    """Initialize SWI-Prolog with proper environment setup"""
    # Set SWI-Prolog environment variables
    swipl_home = r'C:\Program Files\swipl'
    swipl_bin = os.path.join(swipl_home, 'bin')
    swipl_lib = os.path.join(swipl_home, 'lib')
    
    # Important: Set system resources path
    swipl_boot = os.path.join(swipl_home, 'boot.prc')
    if not os.path.exists(swipl_boot):
        swipl_boot = os.path.join(swipl_bin, 'boot.prc')
    
    # Set all required environment variables
    os.environ.update({
        'SWIPL_HOME': swipl_home,
        'SWI_HOME_DIR': swipl_home,
        'SWI_LIB_DIR': swipl_bin,  # Changed to bin where DLL exists
        'SWIPL_BOOT_FILE': swipl_boot,
        'PATH': f"{swipl_bin};{os.environ['PATH']}"
    })
    
    logger.debug("Prolog Environment:")
    for key in ['SWIPL_HOME', 'SWI_HOME_DIR', 'SWI_LIB_DIR', 'SWIPL_BOOT_FILE', 'PATH']:
        logger.debug(f"{key}: {os.environ.get(key)}")
    
    try:
        # Verify critical files
        required_files = {
            'swipl.exe': os.path.join(swipl_bin, 'swipl.exe'),
            'libswipl.dll': os.path.join(swipl_bin, 'libswipl.dll'),
            'boot.prc': swipl_boot
        }
        
        for name, path in required_files.items():
            if not os.path.exists(path):
                raise RuntimeError(f"{name} not found at {path}")
            logger.debug(f"Found {name} at {path}")
        
        # Initialize Prolog
        logger.debug("Initializing Prolog...")
        prolog = Prolog()
        
        # Get absolute path to Prolog file
        prolog_file = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "ruleset",
            "test_recommendations.pl"
        ))
        
        if not os.path.exists(prolog_file):
            raise FileNotFoundError(f"Prolog file not found: {prolog_file}")
            
        logger.debug(f"Loading Prolog file: {prolog_file}")
        prolog.consult(prolog_file)
        
        # Verify Prolog is working
        test_query = list(prolog.query("current_prolog_flag(version, V)"))
        if not test_query:
            raise RuntimeError("Failed to execute test query")
        logger.debug(f"Prolog version: {test_query[0]['V']}")
        
        return prolog
        
    except Exception as e:
        logger.error(f"Prolog initialization failed: {str(e)}")
        raise

# Initialize Prolog
try:
    prolog = init_prolog()
except Exception as e:
    logger.error(f"Fatal error initializing Prolog: {str(e)}")
    sys.exit(1)

class TestRecommendation(BaseModel):
    name: str
    description: str
    normal_range: str
    priority: str

class TestResponse(BaseModel):
    category: str
    tests: List[TestRecommendation]

@app.post("/recommendations")
async def get_recommendations(probability: float) -> TestResponse:
    try:
        logger.debug(f"Executing Prolog query with probability: {probability}")
        query = list(prolog.query(
            f"get_test_recommendations({probability}, Category, Tests)"
        ))
        
        if not query:
            logger.error("No recommendations found")
            raise HTTPException(status_code=404, detail="No recommendations found")
        
        result = query[0]
        logger.debug(f"Query result: {result}")
        
        # Convert Prolog list to Python objects
        tests = []
        for test in result["Tests"]:
            tests.append(TestRecommendation(
                name=str(test[0]),
                description=str(test[1]),
                normal_range=str(test[2]),
                priority=str(test[3])
            ))
        
        return TestResponse(
            category=str(result["Category"]),
            tests=tests
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))