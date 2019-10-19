import torch
import torch.nn as nn
import torchvision.models as models


class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad_(False)
        
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, embed_size)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.embed(features)
        return features
    

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        # implementation for decoderRNN
        super().__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.num_layers = num_layers
        
        # building an Embedding Layer
        # This will convert word to specific vector
        self.embed_word = nn.Embedding(vocab_size, embed_size)
        
        # output of hidden state with hidden size
        self.lstm = nn.LSTM(input_size=embed_size,
                            hidden_size=hidden_size,
                            num_layers=num_layers,
                            dropout=0, # let dropout be 0
                            batch_first=True)
        
        # construct the hidden layer that map the output dimension
        self.hidden2vocab = nn.Linear(hidden_size, vocab_size)
        
    
    def forward(self, features, captions):
        # create embed word vector
        embed_vec = self.embed_word(captions[:,:-1])
        #batchSize,capLength=>batch_size,capLength-1,embedSize
        
        inputs = torch.cat((features.unsqueeze(dim=1), embed_vec), dim=1)

        output_lstm, _ = self.lstm(inputs)
        
        # score
        output = self.hidden2vocab(output_lstm)
        
        # check the shape : 
        
        # print(output_lstm.shape)
        return output
        
        
    def sample(self, inputs, states=None, max_len=20):
        " accepts pre-processed image tensor (inputs) and returns predicted sentence (list of tensor ids of length max_len) "
        caption = []
        
        # To initialize the hidden layer and send it to the same  device as input
        hidden = (torch.randn(self.num_layers, 1, self.hidden_size).to(inputs.device),
                  torch.randn(self.num_layers, 1, self.hidden_size).to(inputs.device))
        
        # Now use this in LSTM output and hidden states to get the caption
        
        for i in range(max_len):
            output_lstm, hidden = self.lstm(inputs, hidden) # batch_size=1, seq_len=1 => 1,1,embedsize
            output = self.hidden2vocab(output_lstm) # 1,1,vocab_size
            output = output.squeeze(1) # 1,vocab_size
            word_id = output.argmax(dim=1) # 1
            caption.append(word_id.item()) # append captions according to ids
            
            # Next to get ready for another next input
            inputs = self.embed_word(word_id.unsqueeze(0)) #(1,1) to (1,1,embed_size)
            
        
        return caption