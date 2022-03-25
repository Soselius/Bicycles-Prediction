clear all;
clc;

load Prediction_onehot_ANN_L12_o1_outputs1_N16.mat
load Prediction_onehot_ANN_L12_o1_outputs1_N64.mat
load Prediction_onehot_ANN_L12_o1_outputs1_N256.mat


prob_seq_N16  = Prediction_onehot_ANN_L12_o1_outputs1_N16(1,:);
pred_ANN_L12_N16 = Prediction_onehot_ANN_L12_o1_outputs1_N16(2,:);
pred_final_N16 = sum(prob_seq_N16.*pred_ANN_L12_N16)*100;

prob_seq_N64  = Prediction_onehot_ANN_L12_o1_outputs1_N64(1,:);
pred_ANN_L12_N64 = Prediction_onehot_ANN_L12_o1_outputs1_N64(2,:);
pred_final_N64 = sum(prob_seq_N64.*pred_ANN_L12_N64)*100;

prob_seq_N256  = Prediction_onehot_ANN_L12_o1_outputs1_N256(1,:);
pred_ANN_L12_N256 = Prediction_onehot_ANN_L12_o1_outputs1_N256(2,:);
pred_final_N256 = sum(prob_seq_N256.*pred_ANN_L12_N256)*100;

figure;

graph = [pred_final_N16;
        pred_final_N64;
        pred_final_N256;];

H = bar(graph,'BarWidth', 1);
H.FaceColor = 'flat'
H.CData(1,:) = [.2 .6 .5]
H.CData(2,:) = [.8 .3 .09]
H.CData(3,:) = [0 0.4470 0.7410]

xt = get(gca, 'XTick');


set(gca, 'XTick', xt, 'XTickLabel', {'N = 16','N = 64', 'N = 256'})
%set(H(0),'Facecolor', 'red')
%set(H(1),'Facecolor', 'green')
%set(H(2),'Facecolor', 'blue')

%xt = get(gca, 'XTick');


%set(gca, 'XTick', xt, 'XTickLabel', {'\Lambda = 4','\Lambda = 20'})


%lgnd = {'N - 16', 'N - 64', 'N - 256'}  ;
%legend(lgnd)

ylabel('Prediction Performance (PP) (%)');
ylim([0 100])
xlim([0.5 3.5])

grid on