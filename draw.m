function draw()
    [num,txt,raw] = xlsread('./Data/reviews_US_no formula.xlsx', 2, 1);
    X = raw(:, [36 2 21 22 40 28]);
    X = cell2mat(X);
    mdl = fitlm(X, cell2mat(raw(:, 8)));
    disp(mdl);
end