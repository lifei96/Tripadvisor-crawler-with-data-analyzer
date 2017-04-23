function draw()
    dataset = csvread('./Data/exclamation_income.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_income_all_cities'));
    disp(mdl);
    
    dataset = csvread('./Data/exclamation_merged_income.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_merged_income_all_cities'));
    disp(mdl);
    
    dataset = csvread('./Data/exclamation_income_New_York_City.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_income_New_York_City'));
    disp(mdl);
    
    dataset = csvread('./Data/exclamation_merged_income_New_York_City.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_merged_income_New_York_City'));
    disp(mdl);
    
    dataset = csvread('./Data/exclamation_income_Los_Angeles.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_income_Los_Angeles'));
    disp(mdl);
    
    dataset = csvread('./Data/exclamation_merged_income_Los_Angeles.csv', 1, 0);
    mdl = fitlm(dataset(:, 1), dataset(:, 2));
    disp(sprintf('\n\nexclamation_merged_income_Los_Angeles'));
    disp(mdl);