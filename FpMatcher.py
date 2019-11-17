class FpMatcher:
    def __init__(self):
        self.segmentator = FpSegmentator(30,150)
        self.enhancer = FpEnhancer(10)
        self.extractor = MnExtractor()
        self.matcher = MnMatcher()

    def match(self, fpImg1, fpImg2):
        segmentedFpImg1 = self.segmentator.segment(fpImg1)
        enhancedFpImg1 = self.enhancer.enhance(segmentedFpImg1, np.ones(segmentedFpImg1.shape)*255)
        mnSet1 = self.extractor.extract(enhancedFpImg1)

        segmentedFpImg2 = self.segmentator.segment(fpImg2)
        enhancedFpImg2 = self.enhancer.enhance(segmentedFpImg2, np.ones(segmentedFpImg2.shape)*255)
        mnSet2 = self.extractor.extract(enhancedFpImg2)

        return self.matcher.match(mnSet1, mnSet2) * 100