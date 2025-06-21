My Experiments

At first, I tried using only one convolutional layer.
	•	I used a kernel size of 3×3, and ReLU as the activation function because it is commonly used and recommended in most CNN examples.
	•	For pooling, I used MaxPooling2D with a pool size of 2×2, since it is the most standard option and also used in the course.
	•	I set the number of filters to 32.
	•	I also used a Dropout rate of 0.5 to reduce overfitting.

With this simple setup, the model reached about 0.7488 accuracy.

Then, I followed the course example and added a second convolutional layer with 64 filters and another max pooling layer. The idea was to help the model learn more detailed features in the image.

With this setup, I got much better results:
Accuracy: 0.9644 – Loss: 0.1575

Next, I added one more convolutional layer, this time with 128 filters to detect even more complex features. I still used Dropout(0.5) at the end.

This gave me:
Accuracy: 0.9613 – Loss: 0.1453

After that, I increased the Dropout rate to 0.6 to see if it would reduce overfitting more strongly.

This time the result was:
Accuracy: 0.9577 – Loss: 0.1672

Observation

Adding a second convolutional layer made a big improvement in accuracy.

Adding a third layer still worked well, but didn’t improve the model much further.

Dropout at 0.5 worked best for regularization. When I increased it to 0.6, the performance dropped slightly. The model became too cautious and may have started to underfit.

Overall, for this dataset, a moderate architecture with two convolutional layers, kernel size 3×3, filters of 32 and 64, pool size 2×2, one dense layer, and a dropout of 0.5 gave the best performance.

I also did many experiments with different kernel size etc. however these resulted worse results.