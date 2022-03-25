clear all;
clc;

load Prediction_onehot_LSTM_L8_o1_outputs1_N16.mat;
load Prediction_onehot_LSTM_L8_o1_outputs1_N64.mat;
load Prediction_onehot_LSTM_L8_o1_outputs1_N256.mat;

figure;
%semilogx(-0.3,-0.3,'g+');
hold on;

%plot(-0.3,-0.3,'*b');
%plot(-0.3,-0.3,'ok');
%plot(-0.3,-0.3,'dm');

%legend('N = 16', 'N = 64', 'N = 256');

semilogx(1:length(Prediction_onehot_LSTM_L8_o1_outputs1_N16(1,:)), cumsum(Prediction_onehot_LSTM_L8_o1_outputs1_N16(1,:)),'*');
semilogx(1:length(Prediction_onehot_LSTM_L8_o1_outputs1_N64(1,:)), cumsum(Prediction_onehot_LSTM_L8_o1_outputs1_N64(1,:)),'.', 'Color', 'red');
semilogx(1:length(Prediction_onehot_LSTM_L8_o1_outputs1_N256(1,:)), cumsum(Prediction_onehot_LSTM_L8_o1_outputs1_N256(1,:)),'x', 'Color', 'green');

legend('N = 16', 'N = 64', 'N = 256');

axis([200 600 0 1])

ylabel('CDF');
xlabel('$S_{\kappa}$','interpreter','latex');

set(findall(gca, 'Type', 'Line'),'LineWidth',0.8);

grid on;