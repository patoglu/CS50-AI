# Analysis

## Layer 6, Head 7

To find out which layer and head recognize phrasal verbs in my sentences, I added two phrasal verbs in each sentence.
My goal was not only to check if the model understands one phrasal verb, because it might get that one by chance, but also to see if it shows the same kind of connection in the second phrasal verb in the same sentence. If there is a clear connection in both, then it is more likely to be a real pattern.

As a result, I found that “Layer 6, Head 7” shows this relationship.
There is a clear attention between the “verb” and the “particle” that form the phrasal verb.

However, this attention is not in the direction of “gave -> up”,
but instead it is “up -> gave”, which is much stronger.

So it seems like the model is thinking:
“What verb is this particle ‘up’ connected to?” → “gave”

Example Sentences:
- He gave up [MASK] and turned down the offer.
- They broke down [MASK] and ran into trouble.

## Layer 3, Head 3

In both sentences, there is strong attention between the words car and bike / motorcycle.
These words are similar nouns. Both are vehicles.
They also come in the same part of the sentence.
The model sees that they are close and go together, so it connects them.
This attention head may help BERT understand when two words are in the same group.

Example Sentences:
- He [MASK] a red car and a blue bike.
- He [MASK] a red car and a blue motorcycle.

