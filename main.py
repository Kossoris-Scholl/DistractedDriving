from Processing import normalizer, rollingmean
from Analysis import knn, rf, svm

############ Configurations #############
process_data = True
num_runs = 20
classifiers = [knn, rf]
#########################################

if process_data:
    normalizer.main()
    rollingmean.main()

# Used for the report to map the classifier to a printable name
classifier_names = {knn: 'KNN', rf: 'RF', svm: 'SVM'}
final_results = {}

# Go through each of the specified classifiers
for classifier in classifiers:
    # Initialize the balanced and unbalanced data sets
    total_unbalanced = {'accuracy': 0, 'mse': 0, 'cfm': 0, 'cross_val_score': 0, 'f1_macro': 0, 'f1_micro': 0,
                        'f1_weighted': 0, 'f1_none': 0}
    total_balanced = {'accuracy': 0, 'mse': 0, 'cfm': 0, 'cross_val_score': 0, 'f1_macro': 0, 'f1_micro': 0,
                      'f1_weighted': 0, 'f1_none': 0}
    # Run through the classifier operations num_runs times
    for i in range(num_runs):
        # Execute the classifier's main function, store results in variables
        unbalanced, balanced = classifier.main()

        # Accumulate the results for the average to be calculated later
        total_unbalanced['accuracy'] += unbalanced['accuracy']
        total_unbalanced['mse'] += unbalanced['mse']
        total_unbalanced['cfm'] += unbalanced['cfm']
        total_unbalanced['cross_val_score'] += unbalanced['cross_val_score']
        total_unbalanced['f1_macro'] += unbalanced['f1_macro']
        total_unbalanced['f1_micro'] += unbalanced['f1_micro']
        total_unbalanced['f1_weighted'] += unbalanced['f1_weighted']
        total_unbalanced['f1_none'] += unbalanced['f1_none']

        total_balanced['accuracy'] += balanced['accuracy']
        total_balanced['mse'] += balanced['mse']
        total_balanced['cfm'] += balanced['cfm']
        total_balanced['cross_val_score'] += balanced['cross_val_score']
        total_balanced['f1_macro'] += balanced['f1_macro']
        total_balanced['f1_micro'] += balanced['f1_micro']
        total_balanced['f1_weighted'] += balanced['f1_weighted']
        total_balanced['f1_none'] += balanced['f1_none']

    # Find averages for balanced and unbalanced data
    for key in total_balanced:
        total_balanced[key] = total_balanced[key]/num_runs

    for key in total_unbalanced:
        total_unbalanced[key] = total_unbalanced[key]/num_runs

    # Store results in final results variable
    final_results[classifier] = [total_unbalanced, total_balanced]

# Print final results for each classifier used
print('--------------FINAL REPORT--------------')
for classifier in classifiers:
    print('--------------', classifier_names[classifier], '--------------')

    print('\n<<< Unbalanced >>>')
    print('Accuracy: ', final_results[classifier][0]['accuracy'])
    print('Mean Square Error: ', final_results[classifier][0]['mse'])
    print('Confusion Matrix: ', final_results[classifier][0]['cfm'])
    print('Cross Validation Score: ', final_results[classifier][0]['cross_val_score'])
    print('F1 Macro: ', final_results[classifier][0]['f1_macro'])
    print('F1 Micro: ', final_results[classifier][0]['f1_micro'])
    print('F1 Weighted: ', final_results[classifier][0]['f1_weighted'])
    print('F1 None: ', final_results[classifier][0]['f1_none'])

    print('\n<<< Balanced >>>')
    print('Accuracy: ', final_results[classifier][1]['accuracy'])
    print('Mean Square Error: ', final_results[classifier][1]['mse'])
    print('Confusion Matrix: ', final_results[classifier][1]['cfm'])
    print('Cross Validation Score: ', final_results[classifier][1]['cross_val_score'])
    print('F1 Macro: ', final_results[classifier][1]['f1_macro'])
    print('F1 Micro: ', final_results[classifier][1]['f1_micro'])
    print('F1 Weighted: ', final_results[classifier][1]['f1_weighted'])
    print('F1 None: ', final_results[classifier][1]['f1_none'])
