class Config:
    def __init__(self):
        self.localPath = "/Users/NA/Desktop/Independent Study/Data/"
        self.fileNames = ["T001.csv"]

        # for x in range(1,10):
        #     self.fileNames.append("T00" + str(x) + ".csv")
        # for x in range (10, 89):
        #     self.fileNames.append("T0" + str(x) + ".csv")

        self.columnNames = ["Time", "Drive",	"Stimulus", "Failure", "Palm.EDA", "Heart.Rate", "Breathing.Rate",
               "Perinasal.Perspiration", "Speed", "Acceleration", "Brake", "Steering", "LaneOffset",
               "Lane.Position", "Distance", "Gaze.X.Pos", "Gaze.Y.Pos", "Lft.Pupil.Diameter", "Rt.Pupil.Diameter"]