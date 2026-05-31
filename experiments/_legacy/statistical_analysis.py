"""
Statistical Analysis Module for Rigorous Scientific Validation
"""

import numpy as np
import scipy.stats as stats
import json
from typing import List, Dict, Tuple

class RigorousStatisticalAnalysis:
    def __init__(self, min_samples: int = 30):
        """
        Initialize with minimum sample size for statistical validity
        Standard: n >= 30 for Central Limit Theorem
        """
        self.min_samples = min_samples
    
    def analyze_performance_data(self, cpp_times: List[float], python_times: List[float]) -> Dict:
        """
        Rigorous statistical analysis of performance data
        """
        results = {}
        
        # 1. SAMPLE SIZE VALIDATION
        if len(cpp_times) < self.min_samples or len(python_times) < self.min_samples:
            results['warning'] = f"Sample size too small (n={min(len(cpp_times), len(python_times))}). Recommend n>={self.min_samples}"
        
        # 2. DESCRIPTIVE STATISTICS
        results['cpp_stats'] = self._descriptive_stats(cpp_times)
        results['python_stats'] = self._descriptive_stats(python_times)
        
        # 3. NORMALITY TESTS
        results['cpp_normality'] = self._test_normality(cpp_times)
        results['python_normality'] = self._test_normality(python_times)
        
        # 4. STATISTICAL SIGNIFICANCE TEST
        results['significance_test'] = self._test_significance(cpp_times, python_times)
        
        # 5. CONFIDENCE INTERVALS
        results['confidence_intervals'] = self._confidence_intervals(cpp_times, python_times)
        
        # 6. EFFECT SIZE
        results['effect_size'] = self._cohens_d(cpp_times, python_times)
        
        # 7. POWER ANALYSIS
        results['power_analysis'] = self._power_analysis(cpp_times, python_times)
        
        return results
    
    def _descriptive_stats(self, data: List[float]) -> Dict:
        """Calculate comprehensive descriptive statistics"""
        arr = np.array(data)
        return {
            'n': len(data),
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr, ddof=1)),  # Sample standard deviation
            'variance': float(np.var(arr, ddof=1)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'q25': float(np.percentile(arr, 25)),
            'q75': float(np.percentile(arr, 75)),
            'iqr': float(np.percentile(arr, 75) - np.percentile(arr, 25)),
            'cv': float(np.std(arr, ddof=1) / np.mean(arr))  # Coefficient of variation
        }
    
    def _test_normality(self, data: List[float]) -> Dict:
        """Test normality using Shapiro-Wilk test"""
        if len(data) < 3:
            return {'error': 'Insufficient data for normality test'}
        
        stat, p_value = stats.shapiro(data)
        return {
            'test': 'Shapiro-Wilk',
            'statistic': float(stat),
            'p_value': float(p_value),
            'is_normal': p_value > 0.05,
            'interpretation': 'Normal distribution' if p_value > 0.05 else 'Non-normal distribution'
        }
    
    def _test_significance(self, cpp_times: List[float], python_times: List[float]) -> Dict:
        """Statistical significance test for difference in means"""
        # Use Mann-Whitney U test (non-parametric) for robustness
        statistic, p_value = stats.mannwhitneyu(cpp_times, python_times, alternative='two-sided')
        
        # Also include t-test for comparison
        t_stat, t_p_value = stats.ttest_ind(cpp_times, python_times)
        
        return {
            'mann_whitney_u': {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'interpretation': 'Statistically significant difference' if p_value < 0.05 else 'No significant difference'
            },
            'welch_t_test': {
                'statistic': float(t_stat),
                'p_value': float(t_p_value),
                'significant': t_p_value < 0.05,
                'interpretation': 'Statistically significant difference' if t_p_value < 0.05 else 'No significant difference'
            }
        }
    
    def _confidence_intervals(self, cpp_times: List[float], python_times: List[float], confidence: float = 0.95) -> Dict:
        """Calculate confidence intervals for means"""
        alpha = 1 - confidence
        
        cpp_ci = stats.t.interval(confidence, len(cpp_times)-1, 
                                  loc=np.mean(cpp_times), 
                                  scale=stats.sem(cpp_times))
        
        python_ci = stats.t.interval(confidence, len(python_times)-1,
                                     loc=np.mean(python_times),
                                     scale=stats.sem(python_times))
        
        # Ratio confidence interval (approximate)
        ratio_mean = np.mean(python_times) / np.mean(cpp_times)
        ratio_std = ratio_mean * np.sqrt((np.std(python_times)/np.mean(python_times))**2 + 
                                         (np.std(cpp_times)/np.mean(cpp_times))**2)
        ratio_ci = (ratio_mean - 1.96*ratio_std, ratio_mean + 1.96*ratio_std)
        
        return {
            'confidence_level': confidence,
            'cpp_mean_ci': [float(cpp_ci[0]), float(cpp_ci[1])],
            'python_mean_ci': [float(python_ci[0]), float(python_ci[1])],
            'ratio_estimate': float(ratio_mean),
            'ratio_ci': [float(ratio_ci[0]), float(ratio_ci[1])],
            'interpretation': f"We are {confidence*100}% confident the true ratio is between {ratio_ci[0]:.3f} and {ratio_ci[1]:.3f}"
        }
    
    def _cohens_d(self, cpp_times: List[float], python_times: List[float]) -> Dict:
        """Calculate Cohen's d effect size"""
        cpp_mean, python_mean = np.mean(cpp_times), np.mean(python_times)
        cpp_std, python_std = np.std(cpp_times, ddof=1), np.std(python_times, ddof=1)
        
        # Pooled standard deviation
        n1, n2 = len(cpp_times), len(python_times)
        pooled_std = np.sqrt(((n1-1)*cpp_std**2 + (n2-1)*python_std**2) / (n1+n2-2))
        
        cohens_d = (python_mean - cpp_mean) / pooled_std
        
        # Interpret effect size
        if abs(cohens_d) < 0.2:
            magnitude = "negligible"
        elif abs(cohens_d) < 0.5:
            magnitude = "small"
        elif abs(cohens_d) < 0.8:
            magnitude = "medium"
        else:
            magnitude = "large"
        
        return {
            'cohens_d': float(cohens_d),
            'magnitude': magnitude,
            'interpretation': f"Effect size is {magnitude} (|d| = {abs(cohens_d):.3f})"
        }
    
    def _power_analysis(self, cpp_times: List[float], python_times: List[float]) -> Dict:
        """Estimate statistical power of the test"""
        effect_size = abs(self._cohens_d(cpp_times, python_times)['cohens_d'])
        n = min(len(cpp_times), len(python_times))
        
        # Approximate power calculation for two-sample t-test
        # This is a simplified version - more complex calculations exist
        delta = effect_size * np.sqrt(n/2)
        power = 1 - stats.norm.cdf(1.96 - delta) + stats.norm.cdf(-1.96 - delta)
        
        return {
            'estimated_power': float(power),
            'sample_size': n,
            'effect_size': float(effect_size),
            'interpretation': f"Power = {power:.3f} ({'adequate' if power > 0.8 else 'inadequate'} for detecting true differences)"
        }

def generate_statistical_report(results_file: str, output_file: str):
    """Generate comprehensive statistical report from experiment results"""
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    analyzer = RigorousStatisticalAnalysis()
    
    # Extract timing data
    cpp_times = [run['time'] for run in data.get('cpp_runs', [])]
    python_times = [run['time'] for run in data.get('python_runs', [])]
    
    if not cpp_times or not python_times:
        print("❌ Error: No timing data found in results file")
        return
    
    # Perform statistical analysis
    analysis = analyzer.analyze_performance_data(cpp_times, python_times)
    
    # Generate report
    report = {
        'experiment': data.get('problem_title', 'Unknown'),
        'complexity_class': data.get('complexity_class', 'Unknown'),
        'raw_data': {
            'cpp_times': cpp_times,
            'python_times': python_times
        },
        'statistical_analysis': analysis,
        'conclusion': _generate_conclusion(analysis)
    }
    
    # Save report
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📊 Statistical report generated: {output_file}")
    return report

def _generate_conclusion(analysis: Dict) -> Dict:
    """Generate scientific conclusion based on statistical analysis"""
    
    significance = analysis['significance_test']['mann_whitney_u']['significant']
    effect_size = analysis['effect_size']['magnitude']
    power = analysis['power_analysis']['estimated_power']
    
    if significance and effect_size in ['medium', 'large'] and power > 0.8:
        conclusion_type = "STRONG_EVIDENCE"
        interpretation = "Strong statistical evidence of performance difference"
    elif significance and effect_size in ['small', 'medium']:
        conclusion_type = "MODERATE_EVIDENCE"
        interpretation = "Moderate statistical evidence of performance difference"
    elif not significance:
        conclusion_type = "NO_EVIDENCE"
        interpretation = "No statistically significant evidence of performance difference"
    else:
        conclusion_type = "WEAK_EVIDENCE"
        interpretation = "Weak or inconclusive evidence"
    
    return {
        'conclusion_type': conclusion_type,
        'interpretation': interpretation,
        'recommendations': _get_recommendations(analysis)
    }

def _get_recommendations(analysis: Dict) -> List[str]:
    """Generate recommendations for improving experimental rigor"""
    recommendations = []
    
    if 'warning' in analysis:
        recommendations.append("Increase sample size to n≥30 for better statistical validity")
    
    if analysis['power_analysis']['estimated_power'] < 0.8:
        recommendations.append("Increase sample size or effect size to achieve adequate statistical power (>0.8)")
    
    if not analysis['cpp_normality']['is_normal'] or not analysis['python_normality']['is_normal']:
        recommendations.append("Consider non-parametric tests due to non-normal distributions")
    
    cv_threshold = 0.1  # 10% coefficient of variation threshold
    if analysis['cpp_stats']['cv'] > cv_threshold or analysis['python_stats']['cv'] > cv_threshold:
        recommendations.append("High variability detected - consider controlling environmental factors")
    
    return recommendations

if __name__ == "__main__":
    # Example usage
    print("🔬 Statistical Analysis Module for Rigorous Scientific Validation")
    print("Usage: from statistical_analysis import generate_statistical_report")
    print("       generate_statistical_report('results.json', 'statistical_report.json')")
