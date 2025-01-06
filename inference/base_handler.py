import time

class InferenceHandler:
    """
    Base class for handling inference of models
    """
    def __init__(self, model_name, temperature):
        """
        Args:
        model_name: The name of the model.
        temperature: temperature of model
        """
        self.model_name = model_name
        self.temperature = temperature


    def inference(self, input_data):
        """
        performs inferences on the pre-processed data
        Args:
        input_data: problem input data
        Returns:
        tool_calls tool calls from inference
        """


    def post_process(self, model_output):
        """
        normalizes tool call output from different apis so they can be properly evaluated
        Args:
        model_output: raw output from model
        Returns:
        processed_data: normalized model output
        """