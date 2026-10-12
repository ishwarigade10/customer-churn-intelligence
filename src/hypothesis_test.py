import os
import pandas as pd
from scipy import stats

def run_hypothesis_tests():
    data_path = os.path.join("data", "customer_features.parquet")
    if not os.path.exists(data_path):
        raise FileNotFoundError("Missing customer_features.parquet. Run src/features.py first.")
    
    df = pd.read_parquet(data_path)
    
    # Filter out customers who didn't leave a review score
    valid_reviews = df.dropna(subset=['avg_review_score'])
    
    churned_scores = valid_reviews[valid_reviews['is_churn'] == 1]['avg_review_score']
    retained_scores = valid_reviews[valid_reviews['is_churn'] == 0]['avg_review_score']
    
    print("=" * 60)
    print("STATISTICAL SUMMARY: REVIEW SCORES")
    print("=" * 60)
    print(f"Churned Customers (n={len(churned_scores):,}):")
    print(f"  Mean:   {churned_scores.mean():.4f}")
    print(f"  Median: {churned_scores.median():.4f}")
    
    print(f"\nRetained Customers (n={len(retained_scores):,}):")
    print(f"  Mean:   {retained_scores.mean():.4f}")
    print(f"  Median: {retained_scores.median():.4f}")
    
    # Perform Mann-Whitney U test (one-sided: churned < retained)
    u_stat, p_val = stats.mannwhitneyu(churned_scores, retained_scores, alternative='less')
    
    print("\n" + "=" * 60)
    print("MANN-WHITNEY U TEST RESULTS")
    print("=" * 60)
    print(f"U-statistic: {u_stat:,.2f}")
    print(f"p-value:     {p_val:.4e}")
    
    alpha = 0.05
    if p_val < alpha:
        print(f"\nConclusion: Reject the Null Hypothesis (p < {alpha}).")
        print("There is statistically significant evidence that churned customers")
        print("give lower review scores than repeat customers.")
    else:
        print(f"\nConclusion: Fail to reject the Null Hypothesis (p >= {alpha}).")
        print("No statistically significant difference observed.")
    print("=" * 60)

if __name__ == "__main__":
    run_hypothesis_tests()