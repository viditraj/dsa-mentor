"""AI/ML interview preparation curriculum data."""

AI_PHASES = {
    1: {
        "name": "ML Foundations",
        "tagline": "Build Your Intuition",
        "description": "Master the core machine learning concepts that every AI/ML interview builds upon. Understand how machines learn from data, the types of learning, and the math that powers it all.",
        "motivation_start": "Every ML engineer starts here. These foundations will make advanced topics feel natural and give you the vocabulary to ace any interview.",
        "estimated_days": 6,
    },
    2: {
        "name": "Core Algorithms & Models",
        "tagline": "Learn the Classics",
        "description": "Dive into the essential ML algorithms from linear models to tree-based methods and SVMs. These are the workhorses of production ML and the most frequently asked topics in interviews.",
        "motivation_start": "Now that you understand the fundamentals, it's time to master the algorithms. Interviewers love asking about trade-offs between these models.",
        "estimated_days": 7,
    },
    3: {
        "name": "Deep Learning & NLP",
        "tagline": "Go Deep",
        "description": "Explore neural networks, CNNs, RNNs, Transformers, and modern NLP. These power the most exciting AI applications today, from ChatGPT to self-driving cars.",
        "motivation_start": "Deep learning is where the magic happens. Understanding these architectures is essential for any modern AI role.",
        "estimated_days": 7,
    },
    4: {
        "name": "ML Systems & Production",
        "tagline": "Ship It to Production",
        "description": "Learn how to take ML models from notebooks to production. Cover MLOps, feature stores, model serving, A/B testing, and the system design of real-world ML platforms.",
        "motivation_start": "Knowing how to build models is only half the battle. Companies want engineers who can deploy, monitor, and scale ML systems in production.",
        "estimated_days": 6,
    },
}

AI_CONCEPTS = [
    # ── Phase 1: ML Foundations ──
    {
        "id": 1,
        "title": "Supervised vs Unsupervised vs Reinforcement Learning",
        "phase": 1,
        "difficulty": "easy",
        "estimated_minutes": 25,
        "frequency": "very_high",
        "tags": ["fundamentals", "learning-paradigms", "basics"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "Supervised: labeled data, predicts outputs (classification/regression). Unsupervised: no labels, finds structure (clustering/dimensionality reduction). Reinforcement: agent learns via rewards by interacting with environment.",
        "explanation": """## Supervised vs Unsupervised vs Reinforcement Learning

The three fundamental paradigms of machine learning define **how** a model learns from data.

### Supervised Learning
You give the model **input-output pairs** (labeled data) and it learns to map inputs to outputs.
- **Classification**: Predict a category (spam vs not spam, cat vs dog)
- **Regression**: Predict a continuous value (house price, temperature)
- Examples: Linear regression, logistic regression, random forests, neural networks
- Requires: Labeled training data (expensive to collect)

### Unsupervised Learning
The model finds **hidden patterns** in data without labels.
- **Clustering**: Group similar data points (K-means, DBSCAN)
- **Dimensionality Reduction**: Compress data while preserving structure (PCA, t-SNE)
- **Anomaly Detection**: Find unusual data points
- Examples: K-means, PCA, autoencoders, DBSCAN
- Requires: Just the data, no labels needed

### Reinforcement Learning
An **agent** takes actions in an **environment** to maximize cumulative **reward**.
- **Agent**: The learner/decision-maker
- **Environment**: What the agent interacts with
- **State**: Current situation
- **Action**: What the agent can do
- **Reward**: Feedback signal (positive or negative)
- Examples: Game AI (AlphaGo), robotics, recommendation systems

### Semi-Supervised & Self-Supervised
- **Semi-supervised**: Small amount of labeled data + large amount of unlabeled data
- **Self-supervised**: Model creates its own labels from the data (e.g., BERT's masked language model)""",
        "key_points": [
            "Supervised learning needs labeled data; unsupervised does not",
            "Classification predicts categories; regression predicts continuous values",
            "Reinforcement learning optimizes cumulative reward through trial and error",
            "Self-supervised learning (used by GPT, BERT) bridges supervised and unsupervised",
            "Most production ML systems use supervised learning",
        ],
        "interview_tips": [
            "Always clarify the problem type first: is this classification, regression, clustering, or RL?",
            "Mention semi-supervised and self-supervised learning to show depth",
            "Relate each paradigm to a real-world example the interviewer can visualize",
        ],
        "common_mistakes": [
            "Confusing classification with clustering - classification has known labels",
            "Assuming unsupervised learning is always inferior to supervised",
            "Forgetting that RL requires a well-defined reward function, which is hard to design",
        ],
        "youtube_keywords": "supervised unsupervised reinforcement learning explained machine learning basics",
        "diagram_description": "Three panels: (1) Supervised - labeled inputs mapped to outputs via model. (2) Unsupervised - unlabeled data grouped into clusters. (3) Reinforcement - agent-environment loop with state, action, reward cycle.",
        "real_world_examples": [
            "Gmail's spam filter uses supervised learning trained on billions of labeled emails",
            "Spotify uses unsupervised clustering to group similar songs for playlist generation",
            "DeepMind's AlphaGo used reinforcement learning to beat the world champion at Go",
        ],
        "related_concepts": [2, 3],
        "practice_questions": [
            "You have customer purchase data but no labels. What type of ML would you use and why?",
            "When would you choose reinforcement learning over supervised learning?",
            "Explain the difference between semi-supervised and self-supervised learning with examples",
        ],
    },
    {
        "id": 2,
        "title": "Bias-Variance Trade-off",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["fundamentals", "model-evaluation", "theory"],
        "companies_asking": ["Google", "Meta", "Amazon", "Netflix", "Apple"],
        "cheat_sheet": "Bias = underfitting (model too simple). Variance = overfitting (model too complex). Total error = bias^2 + variance + irreducible noise. Goal: find the sweet spot. Regularization, cross-validation, and ensemble methods help.",
        "explanation": """## Bias-Variance Trade-off

The **bias-variance trade-off** is one of the most fundamental concepts in ML. It explains why models fail and how to find the right level of complexity.

### Bias (Underfitting)
- **High bias** means the model is too simple to capture the underlying pattern
- The model makes strong assumptions about the data
- Example: Fitting a straight line to data that follows a curve
- Signs: Poor performance on BOTH training and test data

### Variance (Overfitting)
- **High variance** means the model is too complex and memorizes the training data
- The model is sensitive to small fluctuations in the training set
- Example: Fitting a 100-degree polynomial that passes through every training point
- Signs: Great training performance, poor test performance

### The Decomposition
```
Total Error = Bias² + Variance + Irreducible Noise
```
- **Bias²**: Error from wrong assumptions (model too simple)
- **Variance**: Error from sensitivity to training data (model too complex)
- **Irreducible noise**: Inherent randomness in the data (can't be reduced)

### How to Manage the Trade-off
| Problem | Solution |
|---------|----------|
| High bias | More complex model, more features, less regularization |
| High variance | More training data, regularization, dropout, simpler model |
| Both | Ensemble methods (bagging reduces variance, boosting reduces bias) |

### Diagnosing with Learning Curves
- **High bias**: Training and validation error both high, converging together
- **High variance**: Low training error, high validation error, big gap between them""",
        "key_points": [
            "Total error = bias² + variance + irreducible noise",
            "High bias = underfitting; high variance = overfitting",
            "Regularization (L1/L2) reduces variance at the cost of slightly more bias",
            "More training data helps with variance but not with bias",
            "Ensemble methods can reduce both: bagging for variance, boosting for bias",
        ],
        "interview_tips": [
            "Draw learning curves to diagnose bias vs variance problems",
            "Mention the mathematical decomposition to show theoretical depth",
            "Connect to practical solutions: regularization, cross-validation, ensembles",
        ],
        "common_mistakes": [
            "Thinking more data always helps - it only helps with high variance, not high bias",
            "Not using cross-validation to detect overfitting early",
            "Adding more features to a high-variance model (makes it worse)",
        ],
        "youtube_keywords": "bias variance tradeoff machine learning overfitting underfitting explained",
        "diagram_description": "U-shaped curve: x-axis is model complexity, y-axis is error. Training error decreases monotonically. Test error decreases then increases. Optimal point is at the bottom of the test error curve. Left region labeled high bias, right region labeled high variance.",
        "real_world_examples": [
            "Netflix Prize competition showed that ensemble methods (reducing variance) won over complex single models",
            "Google's initial spam filter was too simple (high bias), missing sophisticated spam patterns",
            "Medical diagnosis models must carefully balance - overfitting to training hospital's data fails on other hospitals",
        ],
        "related_concepts": [1, 3, 4],
        "practice_questions": [
            "Your model has 99% training accuracy but 60% test accuracy. What's wrong and how do you fix it?",
            "Explain how regularization addresses the bias-variance trade-off",
            "Why does bagging reduce variance but not bias?",
        ],
    },
    {
        "id": 3,
        "title": "Feature Engineering & Selection",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["fundamentals", "features", "data-preprocessing"],
        "companies_asking": ["Google", "Amazon", "Meta", "Uber", "Airbnb"],
        "cheat_sheet": "Feature engineering creates informative inputs from raw data. Techniques: encoding categoricals (one-hot, target), scaling (standardization, normalization), handling missing values, creating interaction features. Feature selection: filter (correlation), wrapper (RFE), embedded (L1/tree importance).",
        "explanation": """## Feature Engineering & Selection

**Feature engineering** is the art of transforming raw data into inputs that help ML models learn better. It's often the single biggest factor in model performance.

### Key Techniques

#### Handling Categorical Variables
- **One-hot encoding**: Create binary columns for each category (good for <20 categories)
- **Label encoding**: Assign integers (good for ordinal data)
- **Target encoding**: Replace category with mean of target variable (powerful but risk of leakage)
- **Embedding**: Learn dense vector representations (best for high-cardinality)

#### Numeric Transformations
- **Standardization** (Z-score): Mean=0, Std=1 (good for models sensitive to scale: SVM, KNN, neural nets)
- **Min-Max normalization**: Scale to [0, 1] range
- **Log transform**: Handle skewed distributions
- **Binning**: Convert continuous to discrete (age -> age groups)

#### Handling Missing Values
- **Imputation**: Mean, median, mode, or model-based (KNN imputation)
- **Indicator feature**: Add a binary column flagging missing values
- **Drop**: If very few rows are affected

#### Creating New Features
- **Interaction features**: feature_A * feature_B
- **Polynomial features**: x², x³ for non-linear relationships
- **Time-based**: Day of week, hour, is_weekend, time_since_event
- **Aggregation**: Count, mean, sum over groups (user's avg purchase)

### Feature Selection Methods
- **Filter**: Correlation, mutual information, chi-squared (fast, independent of model)
- **Wrapper**: Recursive Feature Elimination - train model, remove weakest feature, repeat
- **Embedded**: L1 regularization (auto-selects), tree-based feature importance""",
        "key_points": [
            "Feature engineering often matters more than model choice for performance",
            "One-hot encoding for low-cardinality categoricals; embeddings for high-cardinality",
            "Always standardize features for distance-based models (SVM, KNN, neural nets)",
            "Target encoding is powerful but requires careful handling to avoid data leakage",
            "L1 regularization performs automatic feature selection by zeroing out coefficients",
        ],
        "interview_tips": [
            "When asked about improving model performance, discuss feature engineering first",
            "Mention domain-specific features - they show you think beyond just algorithms",
            "Discuss feature leakage and how to prevent it (especially with time-series data)",
        ],
        "common_mistakes": [
            "One-hot encoding high-cardinality features (creates thousands of sparse columns)",
            "Not standardizing features before using distance-based models",
            "Target encoding without proper cross-validation (causes data leakage)",
        ],
        "youtube_keywords": "feature engineering machine learning feature selection techniques explained",
        "diagram_description": "Pipeline: Raw Data -> Missing Value Handling -> Encoding Categoricals -> Scaling Numerics -> Creating Interactions -> Feature Selection (filter/wrapper/embedded) -> Final Feature Set fed to Model.",
        "real_world_examples": [
            "Airbnb engineers time-based features (days since last booking, seasonality) for pricing models",
            "Uber creates geospatial features (distance to landmarks, neighborhood stats) for demand prediction",
            "Kaggle competitions are frequently won by creative feature engineering more than model tuning",
        ],
        "related_concepts": [1, 2, 4],
        "practice_questions": [
            "You have a dataset with 500 categorical features, some with 10,000+ categories. How do you encode them?",
            "Explain feature leakage with a concrete example and how to prevent it",
            "How would you engineer features for a fraud detection system?",
        ],
    },
    {
        "id": 4,
        "title": "Model Evaluation Metrics",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["fundamentals", "model-evaluation", "metrics"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Netflix"],
        "cheat_sheet": "Classification: accuracy, precision, recall, F1, AUC-ROC. Regression: MSE, RMSE, MAE, R². Use precision when false positives are costly (spam). Use recall when false negatives are costly (cancer detection). AUC-ROC for ranking. Always use cross-validation.",
        "explanation": """## Model Evaluation Metrics

Choosing the right metric is crucial - **optimizing the wrong metric can make your model useless** in production.

### Classification Metrics

#### Confusion Matrix
```
                Predicted Positive   Predicted Negative
Actual Positive       TP                   FN
Actual Negative       FP                   TN
```

- **Accuracy** = (TP + TN) / Total — misleading with imbalanced classes
- **Precision** = TP / (TP + FP) — "Of predicted positives, how many are correct?"
- **Recall (Sensitivity)** = TP / (TP + FN) — "Of actual positives, how many did we catch?"
- **F1 Score** = 2 * (Precision * Recall) / (Precision + Recall) — harmonic mean
- **AUC-ROC**: Area under the ROC curve; measures ranking quality across all thresholds

#### When to Use What
| Metric | Use When |
|--------|----------|
| Precision | False positives are costly (spam filter, ad targeting) |
| Recall | False negatives are costly (cancer screening, fraud detection) |
| F1 | Need balance between precision and recall |
| AUC-ROC | Need threshold-independent evaluation, ranking quality |

### Regression Metrics
- **MSE (Mean Squared Error)**: Penalizes large errors heavily (squared)
- **RMSE**: Square root of MSE, same unit as target
- **MAE (Mean Absolute Error)**: Robust to outliers, equal penalty for all errors
- **R² (Coefficient of Determination)**: Proportion of variance explained (0 to 1)

### Cross-Validation
Never evaluate on training data. Use **k-fold cross-validation** to get reliable estimates:
1. Split data into k folds
2. Train on k-1 folds, evaluate on the held-out fold
3. Repeat k times, average the results""",
        "key_points": [
            "Accuracy is misleading for imbalanced datasets (99% negative -> always predict negative = 99% accuracy)",
            "Precision-recall trade-off: increasing one typically decreases the other",
            "AUC-ROC is threshold-independent and great for comparing models",
            "Use k-fold cross-validation for reliable evaluation, not a single train-test split",
            "Business context determines the right metric (e.g., recall for medical, precision for spam)",
        ],
        "interview_tips": [
            "Always ask about class balance before choosing a metric",
            "Relate metrics to business impact: 'A false negative here means missing a fraudulent transaction'",
            "Mention stratified k-fold for imbalanced datasets",
        ],
        "common_mistakes": [
            "Using accuracy on imbalanced datasets without considering precision/recall",
            "Not connecting the metric to the business objective",
            "Evaluating on training data instead of using cross-validation",
        ],
        "youtube_keywords": "precision recall F1 AUC ROC model evaluation metrics machine learning",
        "diagram_description": "Confusion matrix with TP, FP, TN, FN quadrants. Arrows show how precision, recall, F1, and accuracy are computed. ROC curve plotted with TPR vs FPR, AUC shaded underneath.",
        "real_world_examples": [
            "Google Search optimizes for precision@10 - the top 10 results should all be relevant",
            "Medical screening prioritizes recall to catch every potential cancer case, accepting some false alarms",
            "Netflix recommendation uses ranking metrics (NDCG) to ensure the best content appears first",
        ],
        "related_concepts": [2, 5, 6],
        "practice_questions": [
            "Your fraud detection model has 99.5% accuracy but only 20% recall. Explain the problem and fix it.",
            "When would you prefer MAE over MSE for regression?",
            "Explain precision-recall trade-off and how to find the optimal threshold",
        ],
    },
    {
        "id": 5,
        "title": "Cross-Validation & Hyperparameter Tuning",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["fundamentals", "model-evaluation", "tuning"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "Cross-validation: k-fold splits data into k parts, trains on k-1, tests on 1, rotates. Stratified k-fold for imbalanced data. Tuning: grid search (exhaustive), random search (efficient), Bayesian optimization (smart). Always tune on validation set, report on test set.",
        "explanation": """## Cross-Validation & Hyperparameter Tuning

### Cross-Validation
A single train-test split can give misleading results. **Cross-validation** gives a more robust estimate of model performance.

#### K-Fold Cross-Validation
1. Shuffle and split data into **k** equal parts (typically k=5 or k=10)
2. For each fold: train on k-1 folds, evaluate on the remaining fold
3. Average the k scores for a final estimate

#### Variants
- **Stratified K-Fold**: Preserves class distribution in each fold (critical for imbalanced data)
- **Leave-One-Out (LOO)**: K = number of samples (expensive but low bias)
- **Time-Series Split**: Respects temporal order — always train on past, test on future
- **Group K-Fold**: Ensures samples from the same group (e.g., same patient) stay together

### Hyperparameter Tuning
Hyperparameters are settings you choose before training (learning rate, number of trees, regularization strength).

#### Methods
- **Grid Search**: Try every combination in a predefined grid. Exhaustive but expensive.
- **Random Search**: Sample random combinations. Often finds good results faster than grid search.
- **Bayesian Optimization**: Use past results to intelligently choose next hyperparameters (Optuna, Hyperopt).
- **Successive Halving / Hyperband**: Start many configs with small budget, keep promising ones.

### Best Practices
```
Data -> [Train/Val/Test Split]
         Train: for model training
         Validation: for hyperparameter tuning (via cross-validation)
         Test: FINAL evaluation only (touch once!)
```
Never tune hyperparameters on the test set — it causes information leakage and overestimates performance.""",
        "key_points": [
            "K-fold cross-validation gives more robust estimates than a single split",
            "Stratified K-fold is essential for imbalanced classification",
            "Random search is often more efficient than grid search for hyperparameter tuning",
            "Bayesian optimization intelligently explores the hyperparameter space",
            "The test set must only be used once for final evaluation, never for tuning",
        ],
        "interview_tips": [
            "Always mention cross-validation when discussing model evaluation",
            "Explain why random search beats grid search (higher-dimensional spaces have many irrelevant dimensions)",
            "For time-series problems, emphasize that random splits leak future information",
        ],
        "common_mistakes": [
            "Using the test set for hyperparameter tuning (information leakage)",
            "Not using stratified folds for imbalanced datasets",
            "Using random k-fold for time-series data instead of temporal splits",
        ],
        "youtube_keywords": "cross validation k-fold hyperparameter tuning grid search random search",
        "diagram_description": "K-fold diagram: data split into 5 blocks, each iteration highlights one test fold and four training folds. Below: grid search vs random search showing grid points vs random points in 2D hyperparameter space.",
        "real_world_examples": [
            "Kaggle winners consistently use stratified k-fold with careful validation strategies",
            "Google uses Vizier, an internal Bayesian optimization service, for hyperparameter tuning at scale",
            "Uber's Michelangelo platform automates hyperparameter tuning for thousands of production models",
        ],
        "related_concepts": [2, 4, 6],
        "practice_questions": [
            "Why is random search often preferred over grid search? Explain mathematically.",
            "How would you set up cross-validation for a time-series forecasting problem?",
            "Explain nested cross-validation and when you'd use it",
        ],
    },
    {
        "id": 6,
        "title": "Regularization (L1, L2, Dropout)",
        "phase": 1,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["fundamentals", "regularization", "overfitting"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Netflix"],
        "cheat_sheet": "Regularization prevents overfitting by penalizing model complexity. L1 (Lasso): adds |w| penalty, produces sparse models (feature selection). L2 (Ridge): adds w² penalty, shrinks weights toward zero. Dropout: randomly disable neurons during training. Early stopping: stop training when validation loss plateaus.",
        "explanation": """## Regularization (L1, L2, Dropout)

**Regularization** techniques prevent overfitting by adding constraints to the model, discouraging it from memorizing the training data.

### L1 Regularization (Lasso)
Adds the **absolute value** of weights to the loss function:
```
Loss = Original Loss + λ * Σ|wᵢ|
```
- Drives some weights exactly to **zero** (automatic feature selection)
- Produces **sparse models** (fewer active features)
- Good when you suspect many features are irrelevant

### L2 Regularization (Ridge)
Adds the **squared** weights to the loss function:
```
Loss = Original Loss + λ * Σwᵢ²
```
- Shrinks all weights toward zero but **never exactly zero**
- Handles correlated features better than L1
- More stable and commonly used as a default

### Elastic Net
Combines L1 and L2:
```
Loss = Original Loss + λ₁ * Σ|wᵢ| + λ₂ * Σwᵢ²
```

### Dropout (Neural Networks)
- Randomly set a fraction of neurons to zero during each training step
- Typical rates: 0.2-0.5 (20-50% of neurons dropped)
- Forces the network to not rely on any single neuron
- Acts like training an ensemble of sub-networks
- **Only active during training**, not inference

### Early Stopping
- Monitor validation loss during training
- Stop when validation loss starts increasing (even if training loss is still decreasing)
- Simple and effective, works for any iterative model

### The λ (Lambda) Hyperparameter
- **λ = 0**: No regularization (risk overfitting)
- **λ too small**: Minimal effect, still overfits
- **λ too large**: Underfitting (model too constrained)
- **Just right**: Tune via cross-validation""",
        "key_points": [
            "L1 produces sparse models (feature selection); L2 shrinks all weights (no sparsity)",
            "Dropout is the standard regularization for neural networks",
            "Early stopping is simple yet effective for any iterative training",
            "Lambda controls regularization strength - tuned via cross-validation",
            "Elastic Net combines benefits of both L1 and L2",
        ],
        "interview_tips": [
            "Explain WHY L1 produces sparsity (the diamond-shaped constraint region)",
            "Connect regularization back to the bias-variance trade-off",
            "Mention that dropout at inference time scales activations to compensate",
        ],
        "common_mistakes": [
            "Applying dropout during inference (must be disabled or scaled)",
            "Using L1 when features are correlated (L2 or Elastic Net is better)",
            "Setting regularization too high, causing severe underfitting",
        ],
        "youtube_keywords": "L1 L2 regularization dropout overfitting machine learning explained",
        "diagram_description": "Two panels: (1) L1 vs L2 constraint regions in 2D weight space - diamond for L1 touching axis (sparse), circle for L2. (2) Neural network with dropout: some neurons crossed out (dropped) during training, all active during inference.",
        "real_world_examples": [
            "Google uses L1 regularization in ad click prediction to select from millions of sparse features",
            "GPT and BERT use dropout (typically 0.1) during pre-training to prevent overfitting",
            "Netflix's recommendation system uses L2 regularization in matrix factorization models",
        ],
        "related_concepts": [2, 4, 5],
        "practice_questions": [
            "Geometrically explain why L1 regularization produces sparse solutions but L2 doesn't",
            "How does dropout act as an ensemble method?",
            "When would you choose Elastic Net over pure L1 or L2?",
        ],
    },
    # ── Phase 2: Core Algorithms & Models ──
    {
        "id": 7,
        "title": "Linear & Logistic Regression",
        "phase": 2,
        "difficulty": "easy",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["algorithms", "linear-models", "regression", "classification"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "Linear regression minimizes MSE for continuous targets. Logistic regression uses sigmoid to output probabilities for classification. Both are linear in parameters, interpretable, and fast. Use regularization (Ridge/Lasso) to prevent overfitting. Logistic uses log-loss (cross-entropy).",
        "explanation": """## Linear & Logistic Regression

These are the foundational models of ML - simple, interpretable, and surprisingly powerful.

### Linear Regression
Predicts a continuous value as a **weighted sum** of features:
```
y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
```
- **Objective**: Minimize Mean Squared Error (MSE)
- **Closed-form solution**: w = (XᵀX)⁻¹Xᵀy (Normal Equation)
- **Gradient descent**: Iteratively update weights (scales to large datasets)
- **Assumptions**: Linear relationship, independent errors, homoscedasticity

### Logistic Regression
Despite the name, it's a **classification** algorithm:
```
P(y=1|x) = σ(wᵀx + b) = 1 / (1 + e^-(wᵀx + b))
```
- **Sigmoid function** squashes output to [0, 1] probability
- **Decision boundary**: Linear (a hyperplane in feature space)
- **Objective**: Minimize log-loss (binary cross-entropy)
- **Multi-class**: One-vs-Rest or Softmax (multinomial logistic)

### Key Differences
| Aspect | Linear Regression | Logistic Regression |
|--------|-------------------|---------------------|
| Task | Regression | Classification |
| Output | Continuous value | Probability [0, 1] |
| Loss | MSE | Log-loss (cross-entropy) |
| Activation | None (identity) | Sigmoid |

### When to Use
- **Baseline model**: Always start here and compare more complex models against it
- **Interpretability needed**: Coefficients directly show feature importance
- **Large datasets**: Scales well, fast training
- **Feature importance**: Regularized logistic regression with L1 for feature selection""",
        "key_points": [
            "Linear regression for continuous targets; logistic regression for classification",
            "Logistic regression outputs probabilities via the sigmoid function",
            "Both are linear in parameters - the decision boundary is always a hyperplane",
            "Always use as a baseline before trying complex models",
            "Regularized variants (Ridge, Lasso) prevent overfitting and enable feature selection",
        ],
        "interview_tips": [
            "Mention that logistic regression is a linear classifier despite using sigmoid",
            "Discuss when linear models beat complex ones (high-dimensional, small data, need interpretability)",
            "Know the closed-form solution and when to use gradient descent instead",
        ],
        "common_mistakes": [
            "Calling logistic regression a 'regression' algorithm - it's classification",
            "Using linear regression for classification (output is unbounded, not a probability)",
            "Forgetting to check linearity assumptions before applying linear regression",
        ],
        "youtube_keywords": "linear regression logistic regression machine learning explained sigmoid",
        "diagram_description": "Left: Linear regression - scatter plot with best-fit line minimizing squared errors. Right: Logistic regression - sigmoid curve mapping linear combination to probability, with decision boundary at 0.5.",
        "real_world_examples": [
            "Google's initial ad click prediction used logistic regression on billions of sparse features",
            "Credit scoring models use logistic regression because regulators require interpretability",
            "Real estate price prediction commonly starts with linear regression as a baseline",
        ],
        "related_concepts": [6, 8, 9],
        "practice_questions": [
            "Why can't we use MSE as the loss function for logistic regression?",
            "When would linear regression outperform a neural network?",
            "Derive the gradient update for logistic regression",
        ],
    },
    {
        "id": 8,
        "title": "Decision Trees & Random Forests",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["algorithms", "tree-models", "ensemble", "classification", "regression"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "Decision trees split data using feature thresholds to maximize information gain (or Gini impurity reduction). Random forests: ensemble of trees trained on bootstrap samples with random feature subsets. Reduces variance via bagging. No feature scaling needed. Handles non-linear relationships.",
        "explanation": """## Decision Trees & Random Forests

### Decision Trees
A tree that makes predictions by learning **if-then rules** from data.

#### How They Work
1. Start with all data at the root
2. Find the **best feature and threshold** to split the data
3. Split criteria: **Information Gain** (entropy) or **Gini Impurity**
4. Repeat recursively until stopping conditions are met

#### Splitting Criteria
- **Gini Impurity**: Gini = 1 - Σpᵢ² (measures class mixture; 0 = pure, 0.5 = max impurity for binary)
- **Information Gain**: IG = Entropy(parent) - Σ(weighted)Entropy(children)
- **For regression**: Minimize variance of target in each node

#### Pros & Cons
- **Pros**: Interpretable, no feature scaling needed, handles non-linear relationships, mixed data types
- **Cons**: Easily overfits, unstable (small data changes -> very different tree), biased toward features with more levels

### Random Forests (Bagging + Random Feature Selection)
An **ensemble** of decision trees that reduces overfitting:
1. Create **B bootstrap samples** (random sampling with replacement)
2. For each sample, train a decision tree with **random feature subset** at each split (typically √p features)
3. **Aggregate predictions**: majority vote (classification) or average (regression)

#### Why It Works
- **Bagging** reduces variance by averaging many high-variance trees
- **Random features** decorrelate the trees (even more variance reduction)
- Result: Low bias (deep trees) + low variance (averaging) = excellent performance

### Feature Importance
Random forests naturally provide feature importance scores:
- **Mean decrease in impurity**: How much each feature reduces Gini/entropy across all splits
- **Permutation importance**: Drop in accuracy when feature values are shuffled""",
        "key_points": [
            "Decision trees are interpretable but prone to overfitting",
            "Random forests use bagging + random features to reduce variance",
            "No feature scaling needed for tree-based models",
            "Feature importance is a built-in benefit of tree-based methods",
            "Random forests rarely overfit with more trees (unlike boosting)",
        ],
        "interview_tips": [
            "Explain Gini impurity vs information gain and when each is preferred",
            "Discuss why random feature selection decorrelates trees (reduces variance further)",
            "Compare random forests with gradient boosting for completeness",
        ],
        "common_mistakes": [
            "Not pruning decision trees (leads to severe overfitting)",
            "Confusing bagging (random forests) with boosting (XGBoost)",
            "Using mean decrease in impurity for importance when features have different scales",
        ],
        "youtube_keywords": "decision tree random forest machine learning ensemble bagging explained",
        "diagram_description": "Left: Single decision tree with feature splits and leaf predictions. Right: Random forest - multiple trees trained on bootstrap samples, predictions aggregated by majority vote/averaging.",
        "real_world_examples": [
            "Airbnb uses random forests for search ranking and pricing suggestions",
            "Microsoft's Kinect body tracking used random forests for real-time pose estimation",
            "Random forests are a top choice in Kaggle competitions for tabular data",
        ],
        "related_concepts": [7, 9, 3],
        "practice_questions": [
            "Explain the difference between bagging and boosting with examples",
            "Why does adding more trees to a random forest not cause overfitting?",
            "How would you handle class imbalance with random forests?",
        ],
    },
    {
        "id": 9,
        "title": "Gradient Boosting (XGBoost, LightGBM)",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["algorithms", "tree-models", "ensemble", "boosting"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Uber"],
        "cheat_sheet": "Boosting trains weak learners sequentially, each correcting predecessor's errors. XGBoost: regularized gradient boosting with tree pruning. LightGBM: leaf-wise growth, faster on large data. CatBoost: handles categoricals natively. Key hyperparams: learning rate, n_estimators, max_depth.",
        "explanation": """## Gradient Boosting (XGBoost, LightGBM)

**Gradient boosting** is one of the most powerful ML algorithms for tabular data. It builds an **ensemble of weak learners** (shallow trees) sequentially, where each new tree corrects the errors of the previous ensemble.

### How Gradient Boosting Works
1. Start with a simple prediction (e.g., mean of target)
2. Compute **residuals** (errors) of current model
3. Fit a new tree to predict these residuals
4. Add the new tree to the ensemble (with a learning rate)
5. Repeat steps 2-4

```
F(x) = F₀(x) + η*h₁(x) + η*h₂(x) + ... + η*hₘ(x)
```
Where η is the learning rate and each hᵢ corrects previous errors.

### XGBoost
- **Regularization**: L1 and L2 on leaf weights (prevents overfitting)
- **Tree pruning**: Max depth + post-pruning
- **Handling missing values**: Learns optimal direction for missing values
- **Parallel processing**: Parallelizes feature-level computation

### LightGBM
- **Leaf-wise growth**: Grows the leaf with max loss reduction (faster convergence)
- **Histogram-based**: Bins continuous features for speed
- **GOSS**: Gradient-based One-Side Sampling (keeps high-gradient samples)
- **Much faster** than XGBoost on large datasets

### CatBoost
- **Native categorical support**: No need for manual encoding
- **Ordered boosting**: Prevents target leakage
- **Works well out-of-the-box** with default hyperparameters

### Key Hyperparameters
| Parameter | Effect |
|-----------|--------|
| learning_rate (η) | Lower = more robust but needs more trees (0.01-0.3) |
| n_estimators | Number of trees (more trees + low LR = better, but slower) |
| max_depth | Tree depth (3-8 typical; deeper = more complex) |
| subsample | Row sampling ratio (0.7-1.0; reduces variance) |
| colsample_bytree | Feature sampling ratio (reduces variance) |""",
        "key_points": [
            "Boosting reduces bias by sequentially correcting errors; bagging reduces variance",
            "XGBoost adds regularization to gradient boosting for better generalization",
            "LightGBM is faster than XGBoost on large datasets due to histogram-based splitting",
            "Learning rate and number of trees have an inverse relationship",
            "Gradient boosting is the go-to algorithm for tabular data in production",
        ],
        "interview_tips": [
            "Explain the difference between bagging (random forest) and boosting clearly",
            "Discuss the learning rate and n_estimators trade-off",
            "Know when gradient boosting fails (very small data, need real-time inference latency)",
        ],
        "common_mistakes": [
            "Setting learning rate too high (overfits quickly with few trees)",
            "Not using early stopping (training too many trees causes overfitting)",
            "Ignoring feature interactions that boosting captures naturally",
        ],
        "youtube_keywords": "XGBoost LightGBM gradient boosting machine learning explained",
        "diagram_description": "Sequential chain: Model 1 predicts -> compute residuals -> Model 2 fits residuals -> updated prediction -> compute new residuals -> Model 3 fits -> ... Final prediction is sum of all models weighted by learning rate.",
        "real_world_examples": [
            "XGBoost has won more Kaggle competitions than any other algorithm for tabular data",
            "Uber uses LightGBM for ETA prediction across millions of trips",
            "Yandex (creator of CatBoost) uses gradient boosting for search ranking",
        ],
        "related_concepts": [8, 2, 6],
        "practice_questions": [
            "Walk through the gradient boosting algorithm step by step",
            "Why is the learning rate important? What happens if it's too high or too low?",
            "Compare XGBoost, LightGBM, and CatBoost - when would you choose each?",
        ],
    },
    {
        "id": 10,
        "title": "Support Vector Machines (SVM)",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["algorithms", "classification", "kernel-methods"],
        "companies_asking": ["Google", "Microsoft", "Amazon", "Apple", "Meta"],
        "cheat_sheet": "SVM finds the hyperplane that maximizes margin between classes. Support vectors are the closest points to the boundary. Kernel trick maps data to higher dimensions for non-linear separation. RBF kernel is default. C controls margin vs error trade-off. Scales poorly to large datasets.",
        "explanation": """## Support Vector Machines (SVM)

SVM finds the **optimal hyperplane** that separates classes with the **maximum margin** (distance between the boundary and the nearest data points).

### Key Concepts

#### Margin and Support Vectors
- **Margin**: Distance between the decision boundary and the nearest data points
- **Support vectors**: The data points closest to the boundary (they define the margin)
- **Goal**: Maximize the margin for better generalization

#### Hard vs Soft Margin
- **Hard margin**: No misclassifications allowed (only works if data is linearly separable)
- **Soft margin**: Allows some misclassifications via slack variables
- **C parameter**: Controls the penalty for misclassification
  - High C: Narrow margin, fewer errors on training data (risk overfitting)
  - Low C: Wide margin, more training errors tolerated (more regularization)

### The Kernel Trick
When data isn't linearly separable, SVM maps it to a **higher-dimensional space** where a linear separator exists - without explicitly computing the transformation.

#### Common Kernels
- **Linear**: K(x,y) = xᵀy — use when data is linearly separable or high-dimensional
- **RBF (Gaussian)**: K(x,y) = exp(-γ||x-y||²) — default, handles non-linear boundaries
- **Polynomial**: K(x,y) = (xᵀy + c)ᵈ — captures polynomial relationships

### Pros and Cons
**Pros**: Effective in high-dimensional spaces, memory efficient (only stores support vectors), robust with proper kernel

**Cons**: Slow on large datasets O(n²-n³), requires feature scaling, not natively probabilistic, hard to interpret""",
        "key_points": [
            "SVM maximizes the margin between classes for better generalization",
            "Support vectors are the critical data points that define the decision boundary",
            "The kernel trick enables non-linear classification without explicit feature mapping",
            "C controls the trade-off between margin width and classification errors",
            "SVMs don't scale well to very large datasets (prefer tree-based methods)",
        ],
        "interview_tips": [
            "Be able to explain the kernel trick intuitively with a visual example",
            "Compare SVM with logistic regression - when each is preferred",
            "Mention that SVMs are less popular now due to scaling issues but still useful for small/medium datasets",
        ],
        "common_mistakes": [
            "Forgetting to scale features before training SVM (mandatory for distance-based)",
            "Using RBF kernel when linear kernel would suffice (simpler = better)",
            "Not tuning both C and gamma for RBF kernel (they interact significantly)",
        ],
        "youtube_keywords": "SVM support vector machine kernel trick margin classification explained",
        "diagram_description": "2D scatter plot with two classes. Hyperplane drawn with maximum margin. Support vectors highlighted on the margin boundaries. Inset shows kernel trick: 2D non-separable data mapped to 3D where a hyperplane separates them.",
        "real_world_examples": [
            "SVMs were state-of-the-art for handwriting recognition (MNIST) before deep learning",
            "Text classification (spam detection) with linear SVM on TF-IDF features remains effective",
            "Bioinformatics uses SVM for protein classification and gene expression analysis",
        ],
        "related_concepts": [7, 6, 11],
        "practice_questions": [
            "Explain the kernel trick with an intuitive example of XOR classification",
            "What's the difference between SVM and logistic regression? When would you choose each?",
            "How does the C parameter affect the SVM decision boundary?",
        ],
    },
    {
        "id": 11,
        "title": "K-Nearest Neighbors & Clustering (K-Means)",
        "phase": 2,
        "difficulty": "easy",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["algorithms", "clustering", "classification", "unsupervised"],
        "companies_asking": ["Google", "Amazon", "Meta", "Spotify", "Netflix"],
        "cheat_sheet": "KNN: classify by majority vote of k nearest neighbors. Lazy learner (no training). K-Means: partition data into k clusters by minimizing within-cluster variance. Choose k via elbow method or silhouette score. Both need feature scaling. KNN is O(n) per prediction.",
        "explanation": """## K-Nearest Neighbors & Clustering (K-Means)

### K-Nearest Neighbors (KNN) - Supervised
A **lazy learning** algorithm that classifies based on the majority vote of the k closest training examples.

#### How It Works
1. Choose k (number of neighbors)
2. For a new point, find the k nearest training points (Euclidean distance)
3. **Classification**: Majority vote among k neighbors
4. **Regression**: Average of k neighbors' values

#### Key Considerations
- **k value**: Small k = complex boundary (overfitting), large k = smooth boundary (underfitting)
- **Distance metric**: Euclidean (default), Manhattan, Minkowski, cosine similarity
- **Feature scaling is critical**: Features with larger ranges dominate distance calculations
- **Curse of dimensionality**: Performance degrades in high dimensions (distances become meaningless)

### K-Means Clustering - Unsupervised
Partitions data into **k clusters** by minimizing within-cluster variance.

#### Algorithm
1. Initialize k cluster centroids (randomly or K-means++)
2. **Assign** each point to the nearest centroid
3. **Update** centroids to the mean of assigned points
4. Repeat steps 2-3 until convergence

#### Choosing k
- **Elbow method**: Plot inertia (within-cluster sum of squares) vs k, look for the "elbow"
- **Silhouette score**: Measures how similar points are to their own cluster vs other clusters (-1 to 1)

#### Limitations
- Assumes **spherical, equally-sized clusters**
- Sensitive to initialization (use K-means++ or run multiple times)
- Must specify k in advance
- Alternatives: DBSCAN (density-based, finds arbitrary shapes), Gaussian Mixture Models (soft assignments)""",
        "key_points": [
            "KNN is a lazy learner - no training phase, all computation at prediction time",
            "Both KNN and K-Means require feature scaling (distance-based)",
            "K-Means assumes spherical clusters; DBSCAN handles arbitrary shapes",
            "Curse of dimensionality makes KNN ineffective in high-dimensional spaces",
            "K-means++ initialization is much better than random initialization",
        ],
        "interview_tips": [
            "Discuss the curse of dimensionality when explaining KNN's limitations",
            "For K-Means, always mention initialization sensitivity and K-means++",
            "Know alternatives: DBSCAN for non-spherical clusters, KD-trees for faster KNN",
        ],
        "common_mistakes": [
            "Not scaling features before KNN or K-Means (leads to biased distances)",
            "Using K-Means for non-spherical or unequally-sized clusters",
            "Choosing k for KNN too small (overfitting) or too large (underfitting)",
        ],
        "youtube_keywords": "KNN K-means clustering machine learning algorithm explained",
        "diagram_description": "Top: KNN classification - new point surrounded by k=5 neighbors with majority vote. Bottom: K-Means iterations - random centroids -> assign points -> update centroids -> converge to final clusters.",
        "real_world_examples": [
            "Spotify clusters users by listening behavior using K-Means for recommendation segments",
            "Amazon uses KNN-style collaborative filtering for product recommendations",
            "Customer segmentation in marketing commonly uses K-Means clustering",
        ],
        "related_concepts": [1, 10, 3],
        "practice_questions": [
            "Why does KNN suffer from the curse of dimensionality?",
            "How would you determine the optimal k for K-Means clustering?",
            "When would you choose DBSCAN over K-Means?",
        ],
    },
    {
        "id": 12,
        "title": "Dimensionality Reduction (PCA, t-SNE)",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["algorithms", "dimensionality-reduction", "unsupervised", "visualization"],
        "companies_asking": ["Google", "Meta", "Amazon", "Netflix", "Apple"],
        "cheat_sheet": "PCA: linear projection onto directions of maximum variance (eigenvectors of covariance matrix). Choose components to retain 95%+ variance. t-SNE: non-linear, preserves local structure for 2D/3D visualization. PCA for preprocessing/compression, t-SNE for visualization only.",
        "explanation": """## Dimensionality Reduction (PCA, t-SNE)

Reducing the number of features while preserving important information. Essential for visualization, noise reduction, and combating the curse of dimensionality.

### PCA (Principal Component Analysis)
A **linear** method that finds the directions of **maximum variance** in the data.

#### How It Works
1. Standardize the data (mean=0, std=1)
2. Compute the **covariance matrix**
3. Find **eigenvectors** (principal components) and **eigenvalues** (variance explained)
4. Sort by eigenvalue, keep top k components
5. Project data onto these k directions

#### Choosing the Number of Components
- **Explained variance ratio**: Keep components until cumulative variance > 95%
- **Scree plot**: Plot eigenvalues, look for the "elbow"

#### Properties
- Components are **orthogonal** (uncorrelated)
- First component captures the most variance
- PCA is **linear** - can't capture non-linear relationships

### t-SNE (t-distributed Stochastic Neighbor Embedding)
A **non-linear** method designed for **visualization** in 2D or 3D.

#### How It Works
1. Compute pairwise similarities in high-dimensional space (Gaussian)
2. Initialize random low-dimensional embedding
3. Compute pairwise similarities in low-dimensional space (t-distribution)
4. Minimize KL divergence between the two similarity distributions

#### Key Differences from PCA
| PCA | t-SNE |
|-----|-------|
| Linear | Non-linear |
| Preserves global structure | Preserves local structure |
| Deterministic | Stochastic (different runs give different results) |
| Fast O(np²) | Slow O(n²) |
| Good for preprocessing | Good for visualization only |
| Invertible | Not invertible |

### UMAP (Uniform Manifold Approximation)
- Modern alternative to t-SNE
- **Faster**, preserves **both local and global** structure better
- Increasingly preferred for visualization""",
        "key_points": [
            "PCA is linear and preserves global variance structure; t-SNE is non-linear and preserves local structure",
            "PCA is used for preprocessing and compression; t-SNE/UMAP for visualization only",
            "Standardize data before PCA (features on different scales bias results)",
            "t-SNE is stochastic - distances between clusters in the plot aren't meaningful",
            "UMAP is becoming the preferred alternative to t-SNE (faster, preserves more structure)",
        ],
        "interview_tips": [
            "Know when to use PCA vs t-SNE vs UMAP and articulate the trade-offs",
            "Mention that t-SNE cluster distances are unreliable (only local structure is preserved)",
            "Discuss PCA as a preprocessing step to remove noise and speed up downstream models",
        ],
        "common_mistakes": [
            "Using t-SNE for anything other than visualization (not suitable for preprocessing)",
            "Interpreting inter-cluster distances in t-SNE plots as meaningful",
            "Applying PCA without standardizing the data first",
        ],
        "youtube_keywords": "PCA t-SNE dimensionality reduction machine learning visualization explained",
        "diagram_description": "Left: PCA - data points in 3D projected onto 2D plane capturing max variance, with principal component arrows shown. Right: t-SNE - high-dimensional clusters mapped to 2D preserving neighborhood relationships.",
        "real_world_examples": [
            "Netflix uses PCA to reduce the dimensionality of user-movie interaction matrices for recommendations",
            "Google uses t-SNE to visualize word embeddings (Word2Vec) showing semantic clusters",
            "Genomics research uses PCA to visualize population genetic structure from millions of genetic variants",
        ],
        "related_concepts": [3, 11, 1],
        "practice_questions": [
            "Explain PCA step-by-step and why we use eigenvectors of the covariance matrix",
            "Why is t-SNE not suitable as a preprocessing step for ML models?",
            "How would you decide the number of principal components to keep?",
        ],
    },
    {
        "id": 13,
        "title": "Naive Bayes & Bayesian Thinking",
        "phase": 2,
        "difficulty": "medium",
        "estimated_minutes": 25,
        "frequency": "high",
        "tags": ["algorithms", "probabilistic", "classification", "bayesian"],
        "companies_asking": ["Google", "Amazon", "Microsoft", "Apple", "Meta"],
        "cheat_sheet": "Naive Bayes applies Bayes' theorem with the 'naive' assumption that features are conditionally independent. P(y|x) ∝ P(x|y)*P(y). Variants: Gaussian (continuous), Multinomial (counts/text), Bernoulli (binary). Fast, great for text classification, works well with small data.",
        "explanation": """## Naive Bayes & Bayesian Thinking

### Bayes' Theorem
The foundation of probabilistic reasoning:
```
P(y|X) = P(X|y) * P(y) / P(X)
```
- **P(y|X)**: Posterior - probability of class y given features X
- **P(X|y)**: Likelihood - probability of features given class
- **P(y)**: Prior - probability of class before seeing data
- **P(X)**: Evidence - normalizing constant

### Naive Bayes Classifier
Applies Bayes' theorem with the **"naive" conditional independence** assumption:
```
P(y|x₁,x₂,...,xₙ) ∝ P(y) * ∏ P(xᵢ|y)
```
Each feature contributes independently to the probability of each class.

### Variants
- **Gaussian NB**: Assumes features follow normal distribution (continuous data)
- **Multinomial NB**: For count data, especially **text classification** (word counts)
- **Bernoulli NB**: For binary features (word presence/absence)

### Why It Works Despite the "Naive" Assumption
- The independence assumption is almost always violated in practice
- But the **ranking of class probabilities** often remains correct
- The **decision boundary** can still be optimal even if probability estimates are wrong
- Works surprisingly well for text classification, spam filtering, and sentiment analysis

### Pros and Cons
**Pros**: Very fast (O(nd) training), works with small data, handles high-dimensional data well, no hyperparameter tuning needed, interpretable

**Cons**: Independence assumption limits accuracy, poor probability calibration, can't learn feature interactions""",
        "key_points": [
            "Naive Bayes assumes features are conditionally independent given the class",
            "Despite the naive assumption, it works well in practice for text and high-dimensional data",
            "Multinomial NB is the go-to baseline for text classification",
            "Training is O(nd) - one of the fastest classifiers",
            "Probability estimates are often poorly calibrated but rankings are usually correct",
        ],
        "interview_tips": [
            "Be able to derive Naive Bayes from Bayes' theorem step by step",
            "Explain WHY it works despite the violated independence assumption",
            "Compare with logistic regression - when each is preferred",
        ],
        "common_mistakes": [
            "Dismissing Naive Bayes as too simple - it's a strong baseline especially for text",
            "Using Gaussian NB for text data instead of Multinomial NB",
            "Trusting the probability outputs without calibration (use Platt scaling or isotonic regression)",
        ],
        "youtube_keywords": "Naive Bayes classifier Bayes theorem machine learning text classification",
        "diagram_description": "Bayes' theorem formula at top. Below: feature vector flowing into Naive Bayes - each feature independently contributes likelihood for each class. Class with highest posterior probability wins.",
        "real_world_examples": [
            "Gmail's first spam filter used Naive Bayes with word frequencies as features",
            "Medical diagnosis systems use Bayesian reasoning to combine symptoms and test results",
            "News article categorization (sports, politics, tech) commonly uses Multinomial Naive Bayes",
        ],
        "related_concepts": [7, 4, 3],
        "practice_questions": [
            "Walk through classifying an email as spam using Naive Bayes with a concrete example",
            "Why does Naive Bayes work despite the independence assumption being violated?",
            "Compare Naive Bayes with logistic regression for text classification",
        ],
    },
    # ── Phase 3: Deep Learning & NLP ──
    {
        "id": 14,
        "title": "Neural Networks & Backpropagation",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 40,
        "frequency": "very_high",
        "tags": ["deep-learning", "neural-networks", "fundamentals"],
        "companies_asking": ["Google", "Meta", "Amazon", "Microsoft", "OpenAI"],
        "cheat_sheet": "Neural nets stack layers of neurons: input -> hidden -> output. Each neuron: z = Wx + b, a = activation(z). Backpropagation computes gradients via chain rule. Activations: ReLU (hidden), sigmoid (binary), softmax (multi-class). Optimizers: SGD, Adam. Batch normalization stabilizes training.",
        "explanation": """## Neural Networks & Backpropagation

### Architecture
A neural network is layers of **neurons** that transform inputs through weighted connections:
```
Input Layer -> Hidden Layer(s) -> Output Layer
```

Each neuron computes:
```
z = W*x + b        (linear transformation)
a = activation(z)   (non-linearity)
```

### Activation Functions
| Function | Formula | Use Case |
|----------|---------|----------|
| ReLU | max(0, z) | Default for hidden layers |
| Sigmoid | 1/(1+e^-z) | Binary classification output |
| Softmax | e^zi/Sum(e^zj) | Multi-class classification output |
| Tanh | (e^z - e^-z)/(e^z + e^-z) | Hidden layers (centered output) |

### Backpropagation
The algorithm for training neural networks:
1. **Forward pass**: Compute predictions layer by layer
2. **Compute loss**: Compare predictions to targets
3. **Backward pass**: Compute gradients using the **chain rule**
4. **Update weights**: w = w - lr * dL/dw

### Optimization
- **SGD**: Update with gradient of random mini-batch
- **Momentum**: Accumulate velocity to escape local minima
- **Adam**: Adaptive learning rate per parameter (most popular)
- **Learning rate scheduling**: Decrease LR over time for fine-tuning

### Key Training Concepts
- **Batch normalization**: Normalize activations between layers (faster, more stable training)
- **Weight initialization**: Xavier (sigmoid/tanh), He (ReLU) - prevents vanishing/exploding gradients
- **Gradient clipping**: Cap gradient magnitude to prevent explosion""",
        "key_points": [
            "Backpropagation uses the chain rule to efficiently compute gradients layer by layer",
            "ReLU is the default activation for hidden layers (simple, avoids vanishing gradient)",
            "Adam optimizer is the default choice (adapts learning rate per parameter)",
            "Batch normalization stabilizes and accelerates training",
            "Proper weight initialization is critical to avoid vanishing/exploding gradients",
        ],
        "interview_tips": [
            "Be able to explain backpropagation with chain rule for a simple 2-layer network",
            "Know why ReLU replaced sigmoid in hidden layers (vanishing gradient problem)",
            "Discuss the universal approximation theorem - neural nets can approximate any function",
        ],
        "common_mistakes": [
            "Using sigmoid in hidden layers (causes vanishing gradients in deep networks)",
            "Not normalizing inputs or using batch normalization",
            "Setting learning rate too high (divergence) or too low (slow convergence)",
        ],
        "youtube_keywords": "neural network backpropagation deep learning explained activation functions",
        "diagram_description": "Multi-layer neural network with input nodes, hidden layers with ReLU activations, and output layer. Forward pass arrows go left-to-right computing predictions. Backward pass arrows go right-to-left computing gradients via chain rule.",
        "real_world_examples": [
            "Google Translate uses deep neural networks to translate between 100+ languages",
            "Tesla's Autopilot uses neural networks for object detection and path planning",
            "DeepMind's AlphaFold uses deep learning to predict protein 3D structures",
        ],
        "related_concepts": [6, 15, 16],
        "practice_questions": [
            "Derive backpropagation for a 2-layer neural network with MSE loss",
            "Why does the vanishing gradient problem occur and how do ReLU and batch norm help?",
            "Compare SGD with momentum vs Adam optimizer",
        ],
    },
    {
        "id": 15,
        "title": "Convolutional Neural Networks (CNN)",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "very_high",
        "tags": ["deep-learning", "cnn", "computer-vision"],
        "companies_asking": ["Google", "Meta", "Apple", "Tesla", "Amazon"],
        "cheat_sheet": "CNNs use convolutional filters to detect spatial patterns in images. Layers: Conv (extract features) -> ReLU -> Pooling (downsample) -> Fully Connected (classify). Key architectures: LeNet, AlexNet, VGG, ResNet (skip connections), EfficientNet. Transfer learning: use pretrained models, fine-tune on your data.",
        "explanation": """## Convolutional Neural Networks (CNN)

CNNs are designed for **spatial data** (images, video) by exploiting **local patterns** and **translation invariance**.

### Key Layers

#### Convolutional Layer
- Slides small **filters** (kernels) across the input
- Each filter detects a specific pattern (edges, textures, shapes)
- **Parameter sharing**: Same filter applied everywhere (reduces parameters dramatically)
- Output size: (W - F + 2P) / S + 1 (W=input, F=filter, P=padding, S=stride)

#### Pooling Layer
- **Max pooling**: Takes max value in each window (most common, 2x2 with stride 2)
- Reduces spatial dimensions (downsampling)
- Provides slight translation invariance

#### Fully Connected Layer
- Flattens the feature maps and classifies
- Final layer uses softmax for multi-class classification

### Architecture Evolution
| Model | Year | Key Innovation |
|-------|------|----------------|
| LeNet | 1998 | First successful CNN (handwritten digits) |
| AlexNet | 2012 | Deep CNN + GPU training, won ImageNet |
| VGG | 2014 | Very deep with small 3x3 filters |
| ResNet | 2015 | Skip connections solve vanishing gradient |
| EfficientNet | 2019 | Compound scaling (depth+width+resolution) |

### ResNet's Skip Connections
```
output = F(x) + x    (identity shortcut)
```
Allows gradients to flow directly through the network, enabling training of 100+ layer networks.

### Transfer Learning
1. Take a model **pretrained on ImageNet** (millions of images)
2. **Freeze** early layers (generic features: edges, textures)
3. **Fine-tune** later layers on your specific dataset
4. Works even with small datasets (few hundred images)""",
        "key_points": [
            "Convolutional layers detect local patterns with shared parameters",
            "Pooling reduces spatial dimensions and adds slight translation invariance",
            "ResNet's skip connections solved vanishing gradients for very deep networks",
            "Transfer learning with pretrained models is the standard approach for computer vision",
            "Early layers learn generic features (edges), deeper layers learn task-specific features",
        ],
        "interview_tips": [
            "Know the output size formula: (W - F + 2P) / S + 1",
            "Explain why parameter sharing makes CNNs efficient vs fully connected layers",
            "Discuss transfer learning as the go-to strategy for limited data scenarios",
        ],
        "common_mistakes": [
            "Training a CNN from scratch on a small dataset (use transfer learning instead)",
            "Not using data augmentation (flips, rotations, crops) to prevent overfitting",
            "Forgetting to resize/normalize images to match pretrained model's input requirements",
        ],
        "youtube_keywords": "CNN convolutional neural network image classification ResNet explained",
        "diagram_description": "Input image -> Conv filters extracting edges -> ReLU -> Max Pooling -> More Conv layers extracting complex features -> Flatten -> Fully Connected -> Softmax output with class probabilities.",
        "real_world_examples": [
            "Google Photos uses CNNs to automatically categorize and search through billions of images",
            "Tesla's Autopilot uses CNNs to detect pedestrians, vehicles, lanes, and traffic signs",
            "Medical imaging: CNNs detect tumors in X-rays and MRIs with accuracy rivaling radiologists",
        ],
        "related_concepts": [14, 16, 20],
        "practice_questions": [
            "Calculate the output dimensions of a Conv layer with specific input, filter, padding, and stride",
            "Explain how ResNet skip connections help train deeper networks",
            "How would you use transfer learning for a dataset with only 500 labeled images?",
        ],
    },
    {
        "id": 16,
        "title": "Recurrent Neural Networks & LSTMs",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 35,
        "frequency": "high",
        "tags": ["deep-learning", "rnn", "sequence-models", "nlp"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "cheat_sheet": "RNNs process sequences by maintaining hidden state. Vanilla RNNs suffer from vanishing gradients. LSTMs add gates (forget, input, output) to control information flow. GRUs are simpler with 2 gates. Bidirectional processes both directions. Largely replaced by Transformers for most NLP tasks.",
        "explanation": """## Recurrent Neural Networks & LSTMs

RNNs are designed for **sequential data** (text, time series, audio) by maintaining a **hidden state** that captures information from previous time steps.

### Vanilla RNN
```
ht = tanh(Wh*ht-1 + Wx*xt + b)
yt = Wy*ht
```
- Processes one element at a time, updating the hidden state
- **Problem**: Vanishing/exploding gradients make it hard to learn long-range dependencies

### LSTM (Long Short-Term Memory)
Solves the vanishing gradient problem with **three gates** and a **cell state**:

#### Gates
- **Forget gate**: Decides what to discard from cell state
- **Input gate**: Decides what new information to store
- **Output gate**: Decides what to output from cell state

The cell state acts as a **highway** for gradients, allowing information to flow across many time steps.

### GRU (Gated Recurrent Unit)
Simplified LSTM with only **two gates** (reset and update):
- Fewer parameters, faster to train
- Performance comparable to LSTM in many tasks

### Bidirectional RNNs
- Process sequence in **both forward and backward** directions
- Captures context from both past and future
- Essential for tasks like named entity recognition

### Limitations
- **Sequential processing**: Can't parallelize (slow training)
- **Fixed context window**: Struggle with very long sequences
- **Largely replaced by Transformers** for NLP (but still used in time-series and edge devices)""",
        "key_points": [
            "RNNs process sequences with hidden state but suffer from vanishing gradients",
            "LSTMs solve this with forget, input, and output gates controlling information flow",
            "GRUs are simpler (2 gates) and often perform comparably to LSTMs",
            "Bidirectional RNNs capture context from both directions",
            "Transformers have largely replaced RNNs for NLP due to parallelization advantages",
        ],
        "interview_tips": [
            "Draw the LSTM cell and explain each gate's purpose",
            "Discuss why Transformers replaced RNNs (parallelization, attention mechanism)",
            "Know that RNNs are still relevant for time-series and on-device inference",
        ],
        "common_mistakes": [
            "Using vanilla RNNs for long sequences (always use LSTM or GRU)",
            "Not using bidirectional RNNs when future context is available",
            "Defaulting to RNNs for NLP when Transformers would be much better",
        ],
        "youtube_keywords": "RNN LSTM GRU recurrent neural network vanishing gradient explained",
        "diagram_description": "Top: Unrolled RNN showing hidden state flowing through time steps. Bottom: LSTM cell diagram with forget gate, input gate, output gate, and cell state highway running through the top.",
        "real_world_examples": [
            "Apple's Siri originally used LSTMs for speech recognition (before switching to Transformers)",
            "Google Translate used bidirectional LSTMs with attention before adopting Transformers",
            "Stock price prediction and weather forecasting still commonly use LSTM models",
        ],
        "related_concepts": [14, 17, 18],
        "practice_questions": [
            "Explain the vanishing gradient problem in RNNs and how LSTMs solve it",
            "Draw an LSTM cell and describe the role of each gate",
            "When would you still choose an LSTM over a Transformer today?",
        ],
    },
    {
        "id": 17,
        "title": "Transformers & Attention Mechanism",
        "phase": 3,
        "difficulty": "hard",
        "estimated_minutes": 45,
        "frequency": "very_high",
        "tags": ["deep-learning", "transformers", "attention", "nlp"],
        "companies_asking": ["Google", "Meta", "OpenAI", "Microsoft", "Amazon"],
        "cheat_sheet": "Transformers use self-attention to process entire sequences in parallel. Attention: Q*K^T/sqrt(d) -> softmax -> *V. Multi-head attention captures different relationship types. Positional encoding adds sequence order. Encoder-decoder (translation), encoder-only (BERT), decoder-only (GPT).",
        "explanation": """## Transformers & Attention Mechanism

The **Transformer** architecture (Vaswani et al., 2017 - "Attention Is All You Need") revolutionized NLP and is now the foundation of modern AI.

### Self-Attention
The core mechanism that allows each token to **attend to every other token** in the sequence:
```
Attention(Q, K, V) = softmax(Q*K^T / sqrt(dk)) * V
```
- **Q (Query)**: What am I looking for?
- **K (Key)**: What do I contain?
- **V (Value)**: What information do I provide?
- **sqrt(dk) scaling**: Prevents dot products from getting too large

### Multi-Head Attention
Instead of one attention function, use **h parallel heads**:
```
MultiHead(Q, K, V) = Concat(head1, ..., headh) * Wo
```
Each head learns to attend to different types of relationships (syntax, semantics, position).

### Transformer Architecture
```
Input Embedding + Positional Encoding
         |
   Multi-Head Self-Attention  <-- residual connection + LayerNorm
         |
   Feed Forward Network       <-- residual connection + LayerNorm
         |
      (repeat N times)
```

### Positional Encoding
Transformers have no built-in notion of sequence order (unlike RNNs). Positional encodings add position information:
- **Sinusoidal**: Fixed sine/cosine functions of different frequencies
- **Learned**: Trainable position embeddings (used in BERT, GPT)

### Architecture Variants
| Type | Examples | Use Case |
|------|----------|----------|
| Encoder-only | BERT | Classification, NER, understanding |
| Decoder-only | GPT | Text generation, language modeling |
| Encoder-Decoder | T5, BART | Translation, summarization |""",
        "key_points": [
            "Self-attention lets each token attend to every other token in parallel",
            "Multi-head attention captures different types of relationships simultaneously",
            "Positional encoding is necessary because Transformers have no inherent order",
            "Residual connections and layer normalization enable training deep Transformers",
            "Attention complexity is O(n^2) with sequence length, driving research into efficient variants",
        ],
        "interview_tips": [
            "Be able to write out the attention formula and explain each component",
            "Discuss the O(n^2) complexity and efforts to reduce it (sparse attention, linear attention)",
            "Know the three main architectures: encoder-only, decoder-only, encoder-decoder",
        ],
        "common_mistakes": [
            "Forgetting the scaling factor sqrt(dk) (leads to vanishing gradients in softmax)",
            "Not understanding why positional encoding is needed (Transformers are permutation-invariant)",
            "Confusing self-attention with cross-attention (self = same sequence, cross = different sequences)",
        ],
        "youtube_keywords": "transformer attention mechanism self-attention BERT GPT explained",
        "diagram_description": "Transformer block: Input -> Multi-Head Self-Attention (with Q, K, V projections and attention weight matrix visualization) -> Add & Norm -> Feed Forward -> Add & Norm -> Output. Multiple blocks stacked.",
        "real_world_examples": [
            "GPT-4 (OpenAI) uses decoder-only Transformer with trillions of parameters",
            "BERT (Google) uses encoder-only Transformer for search ranking and understanding",
            "Google Translate switched from LSTM to Transformer, significantly improving quality",
        ],
        "related_concepts": [16, 18, 19],
        "practice_questions": [
            "Explain self-attention step by step with a concrete example sentence",
            "Why is the attention mechanism O(n^2) and what are approaches to reduce this?",
            "Compare encoder-only vs decoder-only Transformers - when would you use each?",
        ],
    },
    {
        "id": 18,
        "title": "Word Embeddings & Language Models",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["nlp", "embeddings", "language-models"],
        "companies_asking": ["Google", "Meta", "OpenAI", "Amazon", "Microsoft"],
        "cheat_sheet": "Word embeddings map words to dense vectors where similar words are close. Word2Vec (CBOW/Skip-gram), GloVe (co-occurrence matrix). Contextual embeddings (BERT, GPT) give different vectors based on context. LLMs: pretrain on large corpus, fine-tune or prompt for downstream tasks.",
        "explanation": """## Word Embeddings & Language Models

### Word Embeddings
Represent words as **dense vectors** in a continuous space where **semantic similarity corresponds to vector proximity**.

#### Word2Vec
- **CBOW**: Predict center word from surrounding context words
- **Skip-gram**: Predict surrounding words from center word
- Famous property: king - man + woman = queen (approximately)
- Limitation: One embedding per word regardless of context

#### GloVe (Global Vectors)
- Factorizes the word **co-occurrence matrix**
- Captures both local and global statistics
- Often comparable to Word2Vec in practice

### Contextual Embeddings
Modern models give **different embeddings** based on context:

#### BERT (Bidirectional Encoder Representations from Transformers)
- **Pre-training**: Masked Language Model (predict masked words) + Next Sentence Prediction
- **Bidirectional**: Reads text in both directions simultaneously
- **Fine-tuning**: Add task-specific head on top (classification, NER, QA)
- Best for: Understanding tasks (classification, extraction, search)

#### GPT (Generative Pre-trained Transformer)
- **Pre-training**: Autoregressive language modeling (predict next token)
- **Unidirectional**: Only reads left-to-right
- **Few-shot/zero-shot**: Can perform tasks from instructions alone
- Best for: Generation tasks (text, code, conversation)

### Transfer Learning in NLP
1. **Pre-train** on massive unlabeled text corpus (expensive, done once)
2. **Fine-tune** on specific downstream task with labeled data (cheap, fast)
3. Or use **prompting/in-context learning** (GPT-3+) with no fine-tuning""",
        "key_points": [
            "Word2Vec and GloVe give static embeddings; BERT and GPT give contextual embeddings",
            "BERT is bidirectional (good for understanding); GPT is autoregressive (good for generation)",
            "Pre-train on large unlabeled data, then fine-tune or prompt for specific tasks",
            "Embedding dimensions are typically 768 (BERT-base) to 12288 (GPT-4 scale)",
            "Cosine similarity is the standard metric for comparing embeddings",
        ],
        "interview_tips": [
            "Explain the difference between static (Word2Vec) and contextual (BERT) embeddings",
            "Know the pre-training objectives: MLM for BERT, next-token prediction for GPT",
            "Discuss when to fine-tune vs when to use prompting (data availability, task complexity)",
        ],
        "common_mistakes": [
            "Using Word2Vec/GloVe when contextual embeddings (BERT) would be more appropriate",
            "Fine-tuning BERT on very little data without freezing early layers (overfitting)",
            "Not understanding that GPT and BERT have fundamentally different architectures and strengths",
        ],
        "youtube_keywords": "word embeddings Word2Vec BERT GPT language model NLP explained",
        "diagram_description": "Top: Word2Vec - 2D projection showing word clusters (king/queen, man/woman with vector arithmetic). Bottom: BERT architecture - input tokens -> bidirectional Transformer -> contextual embeddings -> task-specific head.",
        "real_world_examples": [
            "Google Search uses BERT to better understand search queries and match results",
            "ChatGPT uses GPT-4 architecture for conversational AI",
            "Spotify uses Word2Vec-style embeddings on playlists to recommend similar songs",
        ],
        "related_concepts": [17, 19, 12],
        "practice_questions": [
            "Explain how Word2Vec Skip-gram model is trained",
            "Why did BERT outperform all previous NLP models? What was the key innovation?",
            "When would you fine-tune a language model vs use it for prompting?",
        ],
    },
    {
        "id": 19,
        "title": "Generative AI (GANs, VAEs, Diffusion)",
        "phase": 3,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "high",
        "tags": ["deep-learning", "generative-models", "computer-vision"],
        "companies_asking": ["Google", "Meta", "OpenAI", "Microsoft", "Adobe"],
        "cheat_sheet": "GANs: generator vs discriminator adversarial game. VAEs: encoder maps to latent space, decoder reconstructs (ELBO loss). Diffusion models: add noise, learn to denoise (DALL-E, Stable Diffusion). Diffusion produces highest quality images. GANs are fast but unstable. VAEs give structured latent space.",
        "explanation": """## Generative AI (GANs, VAEs, Diffusion)

Generative models learn to **create new data** that resembles the training distribution.

### GANs (Generative Adversarial Networks)
Two networks in an **adversarial game**:
- **Generator (G)**: Creates fake data from random noise
- **Discriminator (D)**: Distinguishes real from fake data
- Training: G tries to fool D, D tries to catch G
- **Min-max objective**: min_G max_D [log D(x) + log(1 - D(G(z)))]

#### GAN Challenges
- **Mode collapse**: Generator produces limited variety
- **Training instability**: Balancing G and D is tricky
- **No likelihood estimation**: Hard to evaluate quality objectively

#### GAN Variants
- **DCGAN**: Convolutional architecture (stable training)
- **StyleGAN**: High-quality face generation with style control
- **CycleGAN**: Unpaired image-to-image translation
- **Pix2Pix**: Paired image-to-image translation

### VAEs (Variational Autoencoders)
Encode data into a **structured latent space** and decode back:
- Encoder maps input to a distribution in latent space
- Decoder samples from latent space to reconstruct
- Loss = Reconstruction Loss + KL Divergence
- **Smooth latent space**: Can interpolate between data points

### Diffusion Models (DDPM, Stable Diffusion)
The current state-of-the-art for image generation:
1. **Forward process**: Gradually add Gaussian noise to data over T steps
2. **Reverse process**: Train a neural network to **denoise** step by step
3. **Generation**: Start from pure noise, iteratively denoise to create an image

#### Why Diffusion Models Won
- **Stable training**: No adversarial dynamics
- **High quality**: Better diversity and quality than GANs
- **Controllable**: Easy to condition on text (DALL-E, Stable Diffusion, Midjourney)""",
        "key_points": [
            "GANs use adversarial training (generator vs discriminator) - fast but unstable",
            "VAEs provide structured latent spaces with smooth interpolation but blurrier outputs",
            "Diffusion models are current SOTA: stable training, high quality, controllable",
            "Stable Diffusion and DALL-E use diffusion models conditioned on text prompts",
            "Mode collapse is GANs' biggest challenge; diffusion models avoid it naturally",
        ],
        "interview_tips": [
            "Know the strengths/weaknesses of each: GAN (fast, unstable), VAE (smooth latent, blurry), Diffusion (high quality, slow)",
            "Discuss how text-to-image models work (text encoder + diffusion in latent space)",
            "Mention evaluation metrics: FID (Frechet Inception Distance) for image quality",
        ],
        "common_mistakes": [
            "Thinking GANs are still state-of-the-art for image generation (diffusion models surpassed them)",
            "Not understanding the training instability of GANs (requires careful hyperparameter tuning)",
            "Confusing VAE with a regular autoencoder (VAE has probabilistic latent space with KL term)",
        ],
        "youtube_keywords": "GAN VAE diffusion model generative AI DALL-E Stable Diffusion explained",
        "diagram_description": "Three columns: (1) GAN - Generator and Discriminator in adversarial loop. (2) VAE - Encoder to latent space (Gaussian) to Decoder. (3) Diffusion - image progressively noised, then denoised step by step.",
        "real_world_examples": [
            "DALL-E 3 and Midjourney use diffusion models for text-to-image generation",
            "NVIDIA's StyleGAN generates photorealistic faces that don't exist",
            "Stable Diffusion runs locally, powering open-source creative tools and art generation",
        ],
        "related_concepts": [14, 15, 18],
        "practice_questions": [
            "Explain the GAN training process and the mode collapse problem",
            "How do diffusion models generate images? Walk through the forward and reverse process",
            "Compare GANs, VAEs, and diffusion models - when would you use each?",
        ],
    },
    {
        "id": 20,
        "title": "Transfer Learning & Fine-Tuning",
        "phase": 3,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["deep-learning", "transfer-learning", "fine-tuning", "practical"],
        "companies_asking": ["Google", "Meta", "Amazon", "Microsoft", "OpenAI"],
        "cheat_sheet": "Transfer learning reuses pretrained model knowledge for new tasks. Strategies: feature extraction (freeze all, train head), fine-tuning (unfreeze some/all layers with low LR). LoRA: low-rank adapters for efficient fine-tuning. RLHF: align LLMs with human preferences. Few-shot: learn from examples in the prompt.",
        "explanation": """## Transfer Learning & Fine-Tuning

**Transfer learning** leverages knowledge from a model trained on a large dataset to solve a different (often smaller) task.

### Why Transfer Learning Works
- **Lower layers** learn general features (edges, basic language patterns)
- **Higher layers** learn task-specific features
- Reusing general features saves massive compute and data requirements

### Strategies

#### 1. Feature Extraction
- **Freeze** the entire pretrained model
- Add a new classification/regression head on top
- Only train the new head
- Best when: Very small dataset, similar domain to pretraining

#### 2. Fine-Tuning
- **Unfreeze** some or all layers of the pretrained model
- Train with a **much lower learning rate** than training from scratch
- Gradually unfreeze layers (start from top, work down)
- Best when: Medium dataset, different domain from pretraining

#### 3. Parameter-Efficient Fine-Tuning (PEFT)
Modern LLMs are too large to fully fine-tune. Efficient methods:
- **LoRA (Low-Rank Adaptation)**: Insert small trainable matrices into frozen model layers (trains <1% of parameters)
- **Prefix Tuning**: Prepend learnable virtual tokens to the input
- **Adapters**: Insert small trainable modules between frozen layers
- **QLoRA**: LoRA with quantized base model (fits on consumer GPUs)

#### 4. Prompt-Based Learning
- **Zero-shot**: Describe the task in natural language
- **Few-shot**: Provide a few examples in the prompt
- **Chain-of-thought**: Ask the model to reason step by step

### RLHF (Reinforcement Learning from Human Feedback)
How ChatGPT was aligned with human preferences:
1. Fine-tune on demonstrations (supervised)
2. Train a **reward model** from human preference comparisons
3. Optimize the LLM with PPO to maximize the reward model's score""",
        "key_points": [
            "Transfer learning saves compute and works with limited labeled data",
            "Feature extraction is safest for small datasets; fine-tuning for larger ones",
            "LoRA and QLoRA enable fine-tuning billion-parameter models efficiently",
            "RLHF aligns LLMs with human preferences (key to ChatGPT's success)",
            "Prompt engineering (zero/few-shot) can replace fine-tuning for many tasks",
        ],
        "interview_tips": [
            "Discuss the spectrum: prompting -> LoRA -> full fine-tuning (increasing data/compute)",
            "Know when to fine-tune vs when to use in-context learning",
            "Mention learning rate scheduling (warm-up + cosine decay) for fine-tuning",
        ],
        "common_mistakes": [
            "Using a high learning rate when fine-tuning (destroys pretrained knowledge - catastrophic forgetting)",
            "Fine-tuning the entire model when the dataset is too small (overfits quickly)",
            "Not evaluating whether prompting alone is sufficient before investing in fine-tuning",
        ],
        "youtube_keywords": "transfer learning fine-tuning LoRA RLHF LLM explained",
        "diagram_description": "Spectrum diagram: Left (least data) = zero-shot prompting -> few-shot -> LoRA/PEFT -> full fine-tuning (most data). Below: pretrained model with frozen layers (blue) and trainable layers/adapters (orange).",
        "real_world_examples": [
            "ChatGPT uses RLHF to fine-tune GPT-4 for helpful, harmless, and honest responses",
            "Hugging Face hosts thousands of LoRA adapters for fine-tuning open-source LLMs",
            "Medical imaging uses transfer learning from ImageNet to diagnose diseases with few hundred labeled scans",
        ],
        "related_concepts": [17, 18, 15],
        "practice_questions": [
            "When would you choose LoRA over full fine-tuning? Explain the trade-offs.",
            "Explain RLHF step by step - how is ChatGPT trained to be helpful?",
            "You have 200 labeled images of a rare disease. Design a transfer learning strategy.",
        ],
    },
    # ── Phase 4: ML Systems & Production ──
    {
        "id": 21,
        "title": "ML System Design Framework",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 40,
        "frequency": "very_high",
        "tags": ["ml-systems", "system-design", "production"],
        "companies_asking": ["Google", "Meta", "Amazon", "Microsoft", "Netflix"],
        "cheat_sheet": "ML system design framework: 1) Clarify requirements & metrics, 2) Define ML objective & data, 3) Feature engineering, 4) Model selection & training, 5) Serving & inference, 6) Monitoring & iteration. Always start with business metric, translate to ML metric. Consider offline vs online evaluation.",
        "explanation": """## ML System Design Framework

ML system design interviews test your ability to design **end-to-end ML systems** that solve real business problems.

### The Framework (45-60 min interview)

#### 1. Problem Formulation (5 min)
- Clarify the **business objective**: What problem are we solving?
- Define **success metrics**: Both business (revenue, engagement) and ML (AUC, NDCG)
- Scope: What's in/out of scope? Constraints (latency, privacy, fairness)?

#### 2. Data (5-10 min)
- What data is available? What would we need to collect?
- **Labels**: How do we get ground truth? (explicit feedback, implicit signals, human labeling)
- **Data pipeline**: Batch vs streaming, ETL, data quality checks
- **Data splits**: Train/val/test with temporal awareness (no future leakage)

#### 3. Feature Engineering (10 min)
- **User features**: Demographics, historical behavior, preferences
- **Item features**: Content attributes, popularity, freshness
- **Context features**: Time, device, location
- **Cross features**: User-item interactions, collaborative signals
- Feature store for consistency between training and serving

#### 4. Model Selection & Training (10 min)
- Start simple (logistic regression baseline)
- Progress to complex (gradient boosting, deep learning)
- Training infrastructure: Distributed training, experiment tracking
- Offline evaluation: Cross-validation with appropriate metrics

#### 5. Serving & Inference (10 min)
- **Batch prediction**: Pre-compute for all users/items periodically
- **Online prediction**: Real-time inference for each request
- Model serving: TensorFlow Serving, TorchServe, custom endpoints
- **Latency budget**: Feature computation + model inference < p99 target

#### 6. Monitoring & Iteration (5 min)
- **Online metrics**: A/B testing, business KPIs
- **Model health**: Prediction distribution, feature drift, data quality
- **Feedback loops**: How do predictions influence future data?
- **Retraining cadence**: Scheduled vs triggered by drift detection""",
        "key_points": [
            "Always start with the business objective and translate to an ML formulation",
            "Data quality and feature engineering often matter more than model architecture",
            "Consider the full pipeline: data -> features -> model -> serving -> monitoring",
            "Distinguish offline metrics (AUC) from online metrics (A/B test results)",
            "Address latency, scalability, and fairness proactively",
        ],
        "interview_tips": [
            "Spend the first 5 minutes clarifying requirements - don't jump into modeling",
            "Always discuss both offline evaluation (cross-validation) and online evaluation (A/B test)",
            "Mention feedback loops and how the model's predictions affect future training data",
        ],
        "common_mistakes": [
            "Jumping to model architecture without defining the problem and data clearly",
            "Only discussing the model, ignoring data pipeline, serving, and monitoring",
            "Not addressing how to get labels for training data",
        ],
        "youtube_keywords": "ML system design interview framework machine learning production pipeline",
        "diagram_description": "End-to-end ML pipeline: Data Sources -> Feature Engineering -> Feature Store -> Model Training (offline) -> Model Registry -> Model Serving (online) -> Predictions -> Monitoring Dashboard -> Feedback to Data Sources.",
        "real_world_examples": [
            "Netflix's recommendation system: content + user features -> candidate generation -> ranking model -> A/B tested",
            "Google Search ranking: query + document features -> learning-to-rank model -> served at <200ms latency",
            "Uber's ETA prediction: trip features -> gradient boosting model -> real-time serving -> monitored for drift",
        ],
        "related_concepts": [22, 23, 24],
        "practice_questions": [
            "Design a newsfeed ranking system for a social media platform",
            "Design an ML system for detecting fraudulent transactions in real-time",
            "Walk through the full ML lifecycle for a product recommendation system",
        ],
    },
    {
        "id": 22,
        "title": "Feature Stores & Data Pipelines",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["ml-systems", "data-engineering", "infrastructure"],
        "companies_asking": ["Uber", "Google", "Amazon", "Meta", "Airbnb"],
        "cheat_sheet": "Feature stores provide a centralized registry for ML features, ensuring consistency between training (offline) and serving (online). Components: offline store (batch features in data warehouse), online store (low-latency key-value), feature registry (metadata). Tools: Feast, Tecton, Hopsworks.",
        "explanation": """## Feature Stores & Data Pipelines

### The Problem
Without a feature store:
- **Training-serving skew**: Features computed differently offline vs online
- **Duplicate work**: Multiple teams recompute the same features
- **No discoverability**: Hard to find and reuse existing features
- **Inconsistent data**: Different definitions of the same metric

### Feature Store Architecture

#### Offline Store (Batch Features)
- Stored in data warehouse (BigQuery, Snowflake, S3)
- Computed via batch ETL pipelines (Spark, dbt)
- Used for: Model training, batch predictions, backfill
- Examples: User's 30-day purchase history, item popularity score

#### Online Store (Real-time Features)
- Low-latency key-value store (Redis, DynamoDB)
- Features pre-computed and materialized for serving
- p99 latency < 10ms requirement typical
- Examples: User's last 5 viewed items, real-time session features

#### Streaming Features
- Computed from event streams (Kafka, Kinesis)
- Near real-time aggregations (windowed counts, averages)
- Examples: Clicks in last 5 minutes, rolling fraud score

### Data Pipeline Best Practices
```
Source -> Ingestion -> Validation -> Transformation -> Feature Store -> Model
```

- **Data validation**: Schema checks, distribution monitoring, freshness alerts
- **Backfill capability**: Recompute historical features when logic changes
- **Point-in-time correctness**: Avoid future data leakage in training
- **Lineage tracking**: Know which models use which features""",
        "key_points": [
            "Feature stores ensure consistency between training (offline) and serving (online)",
            "Online store must serve features at low latency (<10ms p99)",
            "Point-in-time correctness prevents future data leakage in training",
            "Feature registry enables discovery and reuse across teams",
            "Streaming features enable near real-time signals from event data",
        ],
        "interview_tips": [
            "Mention training-serving skew as the primary motivation for feature stores",
            "Discuss the trade-off between batch, streaming, and real-time feature computation",
            "Know popular tools: Feast (open-source), Tecton (managed), Uber's Michelangelo",
        ],
        "common_mistakes": [
            "Computing features differently in training and serving pipelines (training-serving skew)",
            "Not ensuring point-in-time correctness when joining features for training data",
            "Ignoring feature freshness - stale features can degrade model performance",
        ],
        "youtube_keywords": "feature store ML data pipeline training serving skew explained",
        "diagram_description": "Feature Store architecture: Batch sources (data warehouse) and streaming sources (Kafka) feed into feature computation. Features stored in offline store (S3/BigQuery) for training and online store (Redis) for serving. Feature registry catalogs all features.",
        "real_world_examples": [
            "Uber's Michelangelo feature store serves features for thousands of ML models in production",
            "Airbnb's Zipline feature store ensures consistent features across search ranking models",
            "Spotify uses a feature store to share user engagement features across recommendation models",
        ],
        "related_concepts": [21, 23, 3],
        "practice_questions": [
            "Design a feature store for a ride-sharing platform's ML models",
            "How would you handle training-serving skew for a real-time fraud detection model?",
            "Explain point-in-time correctness with a concrete example of data leakage",
        ],
    },
    {
        "id": 23,
        "title": "Model Serving & Inference Optimization",
        "phase": 4,
        "difficulty": "hard",
        "estimated_minutes": 35,
        "frequency": "high",
        "tags": ["ml-systems", "inference", "optimization", "deployment"],
        "companies_asking": ["Google", "Amazon", "Meta", "Microsoft", "NVIDIA"],
        "cheat_sheet": "Serving patterns: batch (pre-compute), online (real-time), edge (on-device). Optimization: quantization (FP32->INT8), pruning (remove small weights), distillation (train small model from large), ONNX Runtime. Scaling: horizontal (replicas), GPU sharing, model caching. Target: p99 latency < budget.",
        "explanation": """## Model Serving & Inference Optimization

Getting models into production with **low latency, high throughput, and reliability**.

### Serving Patterns

#### Batch Prediction
- Pre-compute predictions for all entities periodically (hourly/daily)
- Store results in database/cache for fast lookup
- Good for: Recommendations that don't need real-time signals
- Limitation: Stale predictions, no reaction to real-time context

#### Online Prediction
- Compute predictions in real-time for each request
- Features fetched from feature store, model runs inference
- Latency budget: typically 10-100ms p99
- Good for: Search ranking, fraud detection, personalization

#### Edge/On-Device
- Model runs on user's device (phone, browser, IoT)
- Zero network latency, works offline, preserves privacy
- Constraint: Limited compute and memory
- Good for: Mobile keyboard prediction, on-device face detection

### Inference Optimization

#### Quantization
- Reduce precision: FP32 -> FP16 -> INT8
- 2-4x speedup, 2-4x smaller model
- Post-training quantization: No retraining needed
- Quantization-aware training: Better accuracy preservation

#### Pruning
- Remove weights close to zero (structured or unstructured)
- Can remove 50-90% of parameters with minimal accuracy loss
- Structured pruning (entire neurons/filters) is hardware-friendly

#### Knowledge Distillation
- Train a small **student** model to mimic a large **teacher** model
- Student matches teacher's soft probabilities (dark knowledge)
- Example: DistilBERT is 60% smaller, 60% faster, retains 97% of BERT's performance

#### Model Compilation
- **ONNX Runtime**: Cross-framework optimization
- **TensorRT** (NVIDIA): GPU-specific optimizations
- **TorchScript/torch.compile**: PyTorch production optimization""",
        "key_points": [
            "Batch serving for non-real-time needs; online serving for real-time requirements",
            "Quantization (FP32->INT8) gives 2-4x speedup with minimal accuracy loss",
            "Knowledge distillation trains a smaller model to mimic a larger one",
            "Model serving infrastructure must handle auto-scaling, health checks, and rollback",
            "Edge deployment requires aggressive optimization (quantization + pruning + distillation)",
        ],
        "interview_tips": [
            "Always discuss latency budget and how to meet it (caching, optimization, hardware)",
            "Mention canary deployments and A/B testing for safe model rollouts",
            "Know the serving stack: load balancer -> model server -> feature store -> model",
        ],
        "common_mistakes": [
            "Not considering inference latency during model selection (huge model for 10ms budget)",
            "Deploying a new model without canary testing or rollback capability",
            "Forgetting about feature computation latency (often dominates total serving latency)",
        ],
        "youtube_keywords": "model serving inference optimization quantization distillation MLOps",
        "diagram_description": "Request flow: Client -> Load Balancer -> Model Server (GPU/CPU) with Feature Store providing features. Optimization pipeline: Full Model -> Quantization -> Pruning -> Distillation -> Optimized Model for deployment.",
        "real_world_examples": [
            "Google serves BERT-based models at billions of QPS using quantization and custom TPU hardware",
            "Apple runs Core ML models on-device for Face ID, Siri, and keyboard prediction",
            "Tesla runs optimized neural networks on custom FSD chips for real-time self-driving inference",
        ],
        "related_concepts": [21, 22, 24],
        "practice_questions": [
            "Your model takes 500ms per prediction but you need <50ms. What optimizations would you apply?",
            "Design the serving infrastructure for a recommendation model handling 100K QPS",
            "Compare quantization, pruning, and distillation - when would you use each?",
        ],
    },
    {
        "id": 24,
        "title": "A/B Testing & Experiment Design for ML",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "very_high",
        "tags": ["ml-systems", "experimentation", "statistics"],
        "companies_asking": ["Google", "Meta", "Amazon", "Netflix", "Microsoft"],
        "cheat_sheet": "A/B testing: randomly split users into control (old) and treatment (new model). Measure business metrics (CTR, revenue). Statistical significance: p-value < 0.05, sufficient sample size. Watch for: novelty effects, network effects, Simpson's paradox. Use guardrail metrics to catch regressions.",
        "explanation": """## A/B Testing & Experiment Design for ML

A/B testing is the **gold standard** for evaluating ML models in production. Offline metrics (AUC, accuracy) don't always correlate with business impact.

### A/B Testing Fundamentals

#### Setup
1. **Hypothesis**: New ranking model will increase user engagement
2. **Randomization**: Randomly assign users to control (A) or treatment (B)
3. **Metric**: Primary (click-through rate), guardrail (page load time, revenue)
4. **Duration**: Run long enough for statistical significance

#### Statistical Concepts
- **Null hypothesis (H0)**: No difference between A and B
- **p-value**: Probability of observing the data if H0 is true (< 0.05 to reject)
- **Statistical power**: Probability of detecting a real effect (target 80%+)
- **Sample size**: Determined by minimum detectable effect (MDE) and variance
- **Confidence interval**: Range of plausible effect sizes

### ML-Specific Considerations

#### Offline vs Online Evaluation
| Offline | Online (A/B Test) |
|---------|-------------------|
| AUC, F1, RMSE | CTR, revenue, engagement |
| Fast, cheap | Slow, expensive |
| Doesn't capture user behavior | Captures real-world impact |
| Necessary but not sufficient | The ultimate test |

#### Common Pitfalls
- **Novelty effect**: Users engage more initially just because it's new
- **Primacy effect**: Users prefer the familiar (old model)
- **Network effects**: Treatment affects control users indirectly
- **Simpson's paradox**: Overall trend reverses within subgroups
- **Multiple testing**: Running many tests inflates false positives (use Bonferroni correction)

### Advanced Techniques
- **Multi-armed bandits**: Dynamically allocate more traffic to winning variant
- **Interleaving**: Show results from both models mixed together (more sensitive)
- **Switchback experiments**: Alternate between A and B over time (for marketplace effects)""",
        "key_points": [
            "A/B testing is the gold standard for evaluating ML models in production",
            "Offline metrics don't always correlate with online business metrics",
            "Statistical significance (p < 0.05) and sufficient sample size are both required",
            "Guardrail metrics catch regressions in important areas not directly optimized",
            "Novelty effects and network effects can confound A/B test results",
        ],
        "interview_tips": [
            "Always discuss both offline evaluation and A/B testing in ML system design",
            "Mention guardrail metrics to show you think about unintended consequences",
            "Know how to calculate sample size for a given MDE and significance level",
        ],
        "common_mistakes": [
            "Stopping an A/B test early when results look good (peeking problem)",
            "Not accounting for novelty effects (run tests for at least 1-2 weeks)",
            "Using offline metrics alone to decide model deployment",
        ],
        "youtube_keywords": "A/B testing machine learning experiment design statistical significance",
        "diagram_description": "Users randomly split into Control (Model A) and Treatment (Model B). Both serve predictions. Metrics collected and compared. Statistical test determines if difference is significant. Decision: ship, iterate, or rollback.",
        "real_world_examples": [
            "Netflix A/B tests every change to its recommendation algorithm before full rollout",
            "Google runs thousands of search ranking A/B tests per year, each on small user segments",
            "Meta uses multi-armed bandits for ad ranking to quickly converge on the best model",
        ],
        "related_concepts": [21, 25, 4],
        "practice_questions": [
            "Your A/B test shows 2% CTR improvement but p-value is 0.08. What do you do?",
            "How would you design an A/B test for a recommendation model on a marketplace?",
            "Explain the peeking problem and how sequential testing solves it",
        ],
    },
    {
        "id": 25,
        "title": "ML Monitoring & Drift Detection",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["ml-systems", "monitoring", "production", "mlops"],
        "companies_asking": ["Google", "Amazon", "Meta", "Uber", "Netflix"],
        "cheat_sheet": "Monitor: data drift (input distribution changes), concept drift (relationship between features and target changes), model performance degradation. Detection: statistical tests (KS, PSI), distribution comparison. Response: alert, retrain, rollback. Monitor prediction distribution, feature distributions, latency, and business metrics.",
        "explanation": """## ML Monitoring & Drift Detection

ML models degrade over time as the world changes. **Monitoring** detects problems; **drift detection** identifies the root cause.

### Types of Drift

#### Data Drift (Covariate Shift)
- **Input feature distributions** change over time
- Example: User demographics shift, new product categories appear
- Detection: Compare feature distributions between training and production data
- Not always harmful if the model is robust

#### Concept Drift
- The **relationship** between features and target changes
- Example: User preferences change (pandemic behavior), fraud patterns evolve
- Most dangerous: Model's learned patterns become incorrect
- Detection: Monitor prediction accuracy against delayed labels

#### Prediction Drift
- Model's **output distribution** shifts
- Early warning sign even without ground truth labels
- Example: Model suddenly predicts 80% positive when training distribution was 50/50

### Detection Methods
| Method | Detects | How |
|--------|---------|-----|
| Population Stability Index (PSI) | Distribution shift | Compare bucketed distributions |
| Kolmogorov-Smirnov test | Distribution shift | Maximum CDF difference |
| Performance monitoring | Concept drift | Track accuracy over time windows |
| Prediction distribution | All types | Monitor output statistics |

### What to Monitor
1. **Model metrics**: Accuracy, AUC (when delayed labels available)
2. **Prediction distribution**: Mean, variance, percentiles of model outputs
3. **Feature distributions**: Each input feature's statistics
4. **Data quality**: Missing values, schema violations, volume anomalies
5. **System metrics**: Latency, throughput, error rate, GPU utilization
6. **Business metrics**: Revenue, engagement, user satisfaction

### Response Strategies
- **Alert**: Notify ML team when drift exceeds threshold
- **Auto-retrain**: Trigger retraining pipeline on schedule or drift detection
- **Rollback**: Revert to previous model if performance degrades significantly
- **Champion-challenger**: Always have a fallback model ready""",
        "key_points": [
            "Data drift: input distributions change. Concept drift: input-output relationship changes",
            "Monitor prediction distributions as an early warning even without ground truth",
            "PSI and KS tests are standard methods for detecting distribution drift",
            "Delayed labels make real-time accuracy monitoring challenging (use proxy metrics)",
            "Auto-retraining pipelines should be triggered by drift detection, not just schedules",
        ],
        "interview_tips": [
            "Distinguish between data drift and concept drift - they require different responses",
            "Mention that monitoring without ground truth is the real challenge in production",
            "Discuss the full response pipeline: detect -> alert -> diagnose -> retrain -> validate -> deploy",
        ],
        "common_mistakes": [
            "Only monitoring model accuracy without checking feature and prediction distributions",
            "Assuming the model stays accurate forever after deployment",
            "Not having a rollback plan when a model degrades in production",
        ],
        "youtube_keywords": "ML monitoring data drift concept drift model degradation production MLOps",
        "diagram_description": "Dashboard with multiple panels: feature distribution comparison (training vs production), prediction distribution over time, accuracy trend line, data quality checks (green/red indicators). Alert triggers when drift exceeds threshold.",
        "real_world_examples": [
            "Uber's ML models for ETA prediction detect concept drift during holidays and events",
            "Netflix monitors recommendation model performance by comparing online A/B metrics weekly",
            "Financial fraud detection systems must constantly retrain as fraud patterns evolve rapidly",
        ],
        "related_concepts": [21, 24, 26],
        "practice_questions": [
            "How would you detect concept drift in a fraud detection model?",
            "Design a monitoring system for an ML model serving 1M predictions per day",
            "Your model's accuracy dropped 5% over the last month. Walk through your debugging process",
        ],
    },
    {
        "id": 26,
        "title": "Responsible AI: Fairness, Bias & Ethics",
        "phase": 4,
        "difficulty": "medium",
        "estimated_minutes": 30,
        "frequency": "high",
        "tags": ["ml-systems", "fairness", "ethics", "responsible-ai"],
        "companies_asking": ["Google", "Meta", "Amazon", "Microsoft", "Apple"],
        "cheat_sheet": "Bias sources: historical data, sampling, labeling, proxy features. Fairness metrics: demographic parity, equal opportunity, equalized odds. Mitigation: balanced training data, adversarial debiasing, fairness constraints, post-processing thresholds. Interpretability: SHAP, LIME, attention visualization. Always audit models for protected attributes.",
        "explanation": """## Responsible AI: Fairness, Bias & Ethics

ML models can **amplify societal biases** present in training data. Responsible AI ensures models are fair, transparent, and accountable.

### Sources of Bias

#### Data Bias
- **Historical bias**: Training data reflects past discrimination (biased hiring data)
- **Representation bias**: Under-represented groups in training data
- **Measurement bias**: Features measured differently across groups
- **Label bias**: Annotators bring their own biases to labeling

#### Algorithmic Bias
- **Proxy features**: ZIP code as proxy for race, name as proxy for gender
- **Feedback loops**: Biased predictions influence future data collection
- **Optimization bias**: Optimizing overall accuracy sacrifices minority group performance

### Fairness Metrics
| Metric | Definition |
|--------|-----------|
| Demographic Parity | P(positive) is equal across groups |
| Equal Opportunity | TPR is equal across groups |
| Equalized Odds | TPR and FPR are equal across groups |
| Individual Fairness | Similar individuals get similar predictions |

**Important**: These metrics often conflict with each other (impossibility theorems). Choose based on context.

### Mitigation Strategies

#### Pre-processing
- Balance training data across protected groups
- Remove or transform proxy features
- Collect more representative data

#### In-processing
- Add fairness constraints to the optimization objective
- Adversarial debiasing: Train adversary to not predict protected attribute from embeddings
- Fair representation learning

#### Post-processing
- Adjust decision thresholds per group to equalize metrics
- Reject option classification: Defer uncertain cases for human review

### Interpretability & Explainability
- **SHAP (SHapley Additive exPlanations)**: Game-theoretic feature importance per prediction
- **LIME**: Local linear approximation around a prediction
- **Attention visualization**: See what the model focuses on (Transformers)
- **Counterfactual explanations**: What would need to change for a different outcome""",
        "key_points": [
            "Bias in ML comes from data, algorithms, and deployment - not just the model",
            "Fairness metrics often conflict (impossibility theorems) - choose based on context",
            "Proxy features can introduce bias even when protected attributes are removed",
            "SHAP and LIME provide post-hoc explanations for individual predictions",
            "Feedback loops can amplify initial biases over time (predictive policing example)",
        ],
        "interview_tips": [
            "Always mention fairness considerations in ML system design interviews",
            "Know at least 3 fairness metrics and when each is appropriate",
            "Discuss the trade-off between accuracy and fairness honestly",
        ],
        "common_mistakes": [
            "Removing protected attributes and assuming the model is now fair (proxy features remain)",
            "Applying one fairness metric without considering the specific context",
            "Treating fairness as a one-time check rather than continuous monitoring",
        ],
        "youtube_keywords": "AI fairness bias ethics responsible AI SHAP LIME interpretability",
        "diagram_description": "Pipeline: Biased Data -> Model Training -> Biased Predictions -> Real-world Impact -> Feedback Loop back to Data. Intervention points shown at each stage: data balancing, fairness constraints, threshold adjustment, monitoring.",
        "real_world_examples": [
            "Amazon scrapped an AI recruiting tool that discriminated against women (trained on historical hiring data)",
            "COMPAS recidivism prediction system showed significant racial bias in risk scores",
            "Google's Model Cards and Meta's Fairness Flow audit models for bias before deployment",
        ],
        "related_concepts": [21, 25, 4],
        "practice_questions": [
            "Your loan approval model has 90% accuracy overall but 60% for a minority group. How do you address this?",
            "Explain why removing protected attributes doesn't guarantee fairness",
            "Design a fairness audit process for an ML model used in hiring decisions",
        ],
    },
]


# ── Helper Functions ──

def get_ai_concept_by_id(concept_id: int):
    """Get a single concept by its ID."""
    for c in AI_CONCEPTS:
        if c["id"] == concept_id:
            return c
    return None


def get_ai_concepts_by_phase(phase: int):
    """Get all concepts in a given phase."""
    return [c for c in AI_CONCEPTS if c["phase"] == phase]


def get_ai_concepts_by_tag(tag: str):
    """Get all concepts with a given tag."""
    return [c for c in AI_CONCEPTS if tag in c["tags"]]


def get_all_ai_tags():
    """Get all unique tags across all concepts."""
    tags = set()
    for c in AI_CONCEPTS:
        tags.update(c["tags"])
    return sorted(tags)
