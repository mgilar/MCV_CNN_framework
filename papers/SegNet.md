## SegNet
A general semantic segmentation architecture can be broadly thought of as an encoder network followed by a decoder network. The main contribution of SegNet lies is in the manner in which the decoder upsamples its lower resolution input feature maps. Specifically, the decoder uses pooling indices computed in the max-pooling step of the corresponding encoder to perform non-linear upsampling. This eliminates the need for learning to upsample. The upsampled maps are sparse and are then convolved with trainable filters to produce dense feature maps. SegNet is more efficient both in terms of memory and computational time during inference compared to FCN and it is also significantly smaller in the number of trainable parameters.

The key features of this network are:
* The use of unpooling to upsample feature maps in decoder to use and keep high-frequency details intact in the segmentation.
* The encoder doesn’t use the fully connected layers (by convolutionizing them as FCN) and hence is lightweight network lesser parameters.