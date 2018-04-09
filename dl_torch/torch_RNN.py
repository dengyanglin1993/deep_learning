# -*- coding: utf-8 -*-
import torch
import numpy as np
from torch.autograd import Variable
import torchvision as tv
from tensorboardX import SummaryWriter


class PoetryModel(torch.nn.Module):

    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(PoetryModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.embeddings = torch.nn.Embedding(vocab_size, embedding_dim)
        self.lstm = torch.nn.LSTM(embedding_dim, hidden_dim, num_layers=2)
        self.fc1 = torch.nn.Linear(self.hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        seq_len, batch_size = x.size()
        if hidden is None:
            h_0 = x.data.new(2, batch_size, self.hidden_dim).fill_(0).float()
            c_0 = x.data.new(2, batch_size, self.hidden_dim).fill_(0).float()
            h_0, c_0 = Variable(h_0), Variable(c_0)
        else:
            h_0, c_0 = hidden

        embedds = self.embeddings(x)
        output, hidden = self.lstm(embedds, (h_0, c_0))
        output = self.fc1(output.view(seq_len*batch_size,- 1))

        return output, hidden


def main():
    embedding = torch.nn.Embedding(10, 3)
    data = Variable(torch.LongTensor([[1, 2, 4, 5], [4, 3, 2, 9]]))
    print(data,end="\n")
    output = embedding(data)
    print(output)


    embedding1 = torch.nn.Embedding(10, 3,padding_idx=0)
    data1 = Variable(torch.LongTensor([[0,2,0,5]]))
    print(data1,end="\n")
    output1 = embedding1(data1)
    print(output1)

if __name__ == '__main__':
    main()
