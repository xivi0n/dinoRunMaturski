import numpy

def sigmoid(inpt):
    return 1.0/(1.0+numpy.exp(-1*inpt))

def relu(inpt,a):
    result = inpt
    result = [x if x>=0 else a*x for x in inpt]
    #result[inpt<0] = 0
    return result

def predict_label(weights_mat, data_input, activation="relu"):
    r1 = data_input
    for curr_weights in weights_mat:
        r1 = numpy.matmul(r1, curr_weights)
        if activation == "relu":
                r1 = relu(r1,0.01)
        elif activation == "sigmoid":
                r1 = sigmoid(r1)
    predicted_label = numpy.where(r1 == numpy.max(r1))[0][0]
    return predicted_label

def predict_outputs(weights_mat, data_inputs, data_outputs, activation="relu"):
    predictions = numpy.zeros(shape=(data_inputs.shape[0]))
    for sample_idx in range(data_inputs.shape[0]):
        # r1 = data_inputs[sample_idx, :]
        # for curr_weights in weights_mat:
        #     r1 = numpy.matmul(r1, curr_weights)
        #     if activation == "relu":
        #         r1 = relu(r1)
        #     elif activation == "sigmoid":
        #         r1 = sigmoid(r1)
        # predicted_label = numpy.where(r1 == numpy.max(r1))[0][0]
        data_input = data_inputs[sample_idx, :]
        predictions[sample_idx] = predict_label(weights_mat, data_input, activation=activation)
    correct_predictions = numpy.where(predictions == data_outputs)[0].size
    accuracy = (correct_predictions/data_outputs.size)*100
    return accuracy, predictions


def fitness(weights_mat, data_inputs, data_outputs, activation="relu"):
    accuracy = numpy.empty(shape=(weights_mat.shape[0]))
    for sol_idx in range(weights_mat.shape[0]):
        curr_sol_mat = weights_mat[sol_idx, :]
        accuracy[sol_idx], _ = predict_outputs(curr_sol_mat, data_inputs, data_outputs, activation=activation)
    return accuracy

