clear all;
clc;

load Prediction_onehot_LSTM_L8_o1_outputs1_N16.mat
load Prediction_onehot_LSTM_L8_o1_outputs1_N64.mat
load Prediction_onehot_LSTM_L8_o1_outputs1_N256.mat

load Prediction_onehot_LSTM_L8_o1_outputs3_N16.mat
load Prediction_onehot_LSTM_L8_o1_outputs3_N64.mat
load Prediction_onehot_LSTM_L8_o1_outputs3_N256.mat



prob_seq_N16  = Prediction_onehot_LSTM_L8_o1_outputs1_N16(1,:);
pred_LSTM_L8_N16 = Prediction_onehot_LSTM_L8_o1_outputs1_N16(2,:);
pred_final_N16 = sum(prob_seq_N16.*pred_LSTM_L8_N16)*100;

prob_seq_N64  = Prediction_onehot_LSTM_L8_o1_outputs1_N64(1,:);
pred_LSTM_L8_N64 = Prediction_onehot_LSTM_L8_o1_outputs1_N64(2,:);
pred_final_N64 = sum(prob_seq_N64.*pred_LSTM_L8_N64)*100;

prob_seq_N256  = Prediction_onehot_LSTM_L8_o1_outputs1_N256(1,:);
pred_LSTM_L8_N256 = Prediction_onehot_LSTM_L8_o1_outputs1_N256(2,:);
pred_final_N256 = sum(prob_seq_N256.*pred_LSTM_L8_N256)*100;

%%%%%%%%%%%%%%%%%multiple outputs%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

prob_seq_N16_outputs3 = Prediction_onehot_LSTM_L8_o1_outputs3_N16(1,:);
pred_LSTM_L8_N16_outputs3 = Prediction_onehot_LSTM_L8_o1_outputs3_N16(2,:);
pred_final_N16_outputs3 = sum(prob_seq_N16_outputs3.*pred_LSTM_L8_N16_outputs3)*100;

prob_seq_N64_outputs3 = Prediction_onehot_LSTM_L8_o1_outputs3_N64(1,:);
pred_LSTM_L8_N64_outputs3 = Prediction_onehot_LSTM_L8_o1_outputs3_N64(2,:);
pred_final_N64_outputs3 = sum(prob_seq_N64_outputs3.*pred_LSTM_L8_N64_outputs3)*100;

prob_seq_N256_outputs3  = Prediction_onehot_LSTM_L8_o1_outputs3_N256(1,:);
pred_LSTM_L8_N256_outputs3 = Prediction_onehot_LSTM_L8_o1_outputs3_N256(2,:);
pred_final_N256_outputs3 = sum(prob_seq_N256_outputs3.*pred_LSTM_L8_N256_outputs3)*100;

figure;

graph = [pred_final_N16 pred_final_N64 pred_final_N256];

H = bar(graph,'BarWidth', 1);
H.FaceColor = 'flat'
H.CData(1,:) = [.2 .6 .5]
H.CData(2,:) = [.8 .3 .09]
H.CData(3,:) = [0 0.4470 0.7410]

xt = get(gca, 'XTick');


set(gca, 'XTick', xt, 'XTickLabel', {'N = 16','N = 64', 'N = 256'})

%lgnd = {'N - 16', 'N - 64', 'N - 256'}  ;
%legend(lgnd)

ylabel('Prediction Performance (PP) (%)');
ylim([0 100])
xlim([0.5 3.5])

grid on

figure;

graph = [pred_final_N16_outputs3 pred_final_N64_outputs3 pred_final_N256_outputs3];

H = bar(graph,'BarWidth', 1);

%lgnd = {'N - 16', 'N - 64', 'N - 256'}  ;
%legend(lgnd)

ylabel('Prediction Performance (PP) (%)');
ylim([0 100])
xlim([0.5 3.5])

grid on