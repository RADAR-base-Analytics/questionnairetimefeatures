import pandas as pd
from radarpipeline.datalib import RadarData
from radarpipeline.features import Feature, FeatureGroup


class QuestionnaireDataAnalyses(FeatureGroup):
    def __init__(self):
        name = "QuestionnaireDataAnalyses"
        description = "contains Questionnaire Data Features"
        features = [QuestionnaireNotificationResponseLatency, QuestionnaireCompletionTime]
        super().__init__(name, description, features)

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        all_ques_list = {}
        for key in self.required_input_data:
            all_ques_list[key] = data.get_combined_data_by_variable(key)[['key.projectId', 'key.userId', 'key.sourceId', 'value.time',
                                        'value.timeCompleted', 'value.timeNotification', 'value.name']]
        df_ques_app_event = pd.concat(all_ques_list.values()).reset_index(drop=True)
        df_ques_app_event['value.time'] = pd.to_datetime(df_ques_app_event['value.time'], unit="s")
        df_ques_app_event['value.timeNotification'] = pd.to_datetime(df_ques_app_event['value.timeNotification'], unit="s")
        df_ques_app_event['value.timeCompleted'] = pd.to_datetime(df_ques_app_event['value.timeCompleted'], unit="s")
        print(df_ques_app_event)
        df_ques_app_event = df_ques_app_event.rename({"key.userId" : "uid", "value.time" : "time", "value.timeNotification": "time_notification",
                                                            "value.timeCompleted": "time_completed", "value.name":"name"}, axis=1)
        df_ques_app_event = df_ques_app_event.drop_duplicates(subset=["uid", "time", "name"]).reset_index(drop=True)
        df_ques_app_event["date"] = df_ques_app_event["time"].dt.date
        df_ques_app_event = df_ques_app_event.sort_values(by=["uid", "time_notification", "time_completed"]).reset_index(drop=True)
        return df_ques_app_event

    def compute_features(self, data: RadarData) -> RadarData:
        """
        compute and combine the features for each feature in the group.
        """
        pass

class QuestionnaireNotificationResponseLatency(Feature):
    def __init__(self):
        self.name = "QuestionnaireNotificationResponseLatency"
        self.description = "The time it took for participants to start filling out the questionnaires after receiving the notification."
        ## For ART-Pilot analyses
        # self.required_input_data = ["questionnaire_ari_self", "questionnaire_gad7", "questionnaire_phq8", "questionnaire_rpq", "questionnaire_baars_iv"]
        ## For mock data
        self.required_input_data = ["questionnaire_esm","questionnaire_phq8","questionnaire_rses"]

    def preprocess(self, data):
        """
        Preprocess the data for each feature in the group.
        """
        return data

    def calculate(self, data) -> float:
        df_ques_app_event = data
        df_ques_app_event_summary = df_ques_app_event.groupby(["uid", "time_notification"]).agg({"time": min, "time_completed":max}).reset_index().rename({"time":"start_time", "time_completed":"finished_time"}, axis=1)
        df_ques_app_event_summary["notification_response_time"] = df_ques_app_event_summary["start_time"] - df_ques_app_event_summary["time_notification"]
        df_ques_app_event_summary["total_completion_time"] = df_ques_app_event_summary["finished_time"] - df_ques_app_event_summary["time_notification"]
        df_ques_app_event_summary["notification_response_time_sec"] = df_ques_app_event_summary["notification_response_time"].dt.total_seconds()
        return df_ques_app_event_summary




class QuestionnaireCompletionTime(Feature):
    def __init__(self):
        self.name = "QuestionnaireCompletionTime"
        self.description = "The time it took for participants to finish the questionnaires after starting them. "
        ## For ART-Pilot analyses
        # self.required_input_data = ["questionnaire_ari_self", "questionnaire_gad7", "questionnaire_phq8", "questionnaire_rpq", "questionnaire_baars_iv"]
        ## For mock data
        self.required_input_data = ["questionnaire_esm","questionnaire_phq8","questionnaire_rses"]

    def preprocess(self, data):
        """
        Preprocess the data for each feature in the group.
        """
        return data

    def calculate(self, data) -> float:
        df_ques_app_event = data
        df_ques_app_event_summary = df_ques_app_event.groupby(["uid", "time_notification"]).agg({"time": min, "time_completed":max}).reset_index().rename({"time":"start_time", "time_completed":"finished_time"}, axis=1)
        df_ques_app_event_summary["questionnaire_completion_time"] = df_ques_app_event_summary["finished_time"] - df_ques_app_event_summary["start_time"]
        df_ques_app_event_summary["questionnaire_completion_time_sec"] = df_ques_app_event_summary["questionnaire_completion_time"].dt.total_seconds()
        return df_ques_app_event_summary