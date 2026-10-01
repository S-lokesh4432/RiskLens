"""
Standalone Evaluation Runner Script.
Run: python evaluate.py
"""

import json
from src.engine.evaluator import ModelEvaluator

if __name__ == "__main__":
    print("Running NLP Risk Engine Evaluation Benchmark...")
    evaluator = ModelEvaluator()
    res = evaluator.run_evaluation()
    print("\n--- BENCHMARK EVALUATION RESULTS ---")
    print(json.dumps(res, indent=2))
