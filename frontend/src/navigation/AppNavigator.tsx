import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import { ConsultationState } from "../types/consultation";
import { FinalReportScreen } from "../screens/FinalReportScreen";
import { PatientCaseScreen } from "../screens/PatientCaseScreen";
import { PatientQuestionsScreen } from "../screens/PatientQuestionsScreen";
import { PhysicianReviewScreen } from "../screens/PhysicianReviewScreen";

export type RootStackParamList = {
  PatientCase: undefined;
  PatientQuestions: { consultation: ConsultationState };
  PhysicianReview: { consultation: ConsultationState };
  FinalReport: { consultation: ConsultationState };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: "#f8fafc" },
          headerTintColor: "#0f172a",
          headerTitleStyle: { fontWeight: "700" },
          contentStyle: { backgroundColor: "#f8fafc" },
        }}
      >
        <Stack.Screen
          name="PatientCase"
          component={PatientCaseScreen}
          options={{ title: "Cas patient" }}
        />
        <Stack.Screen
          name="PatientQuestions"
          component={PatientQuestionsScreen}
          options={{ title: "Questions" }}
        />
        <Stack.Screen
          name="PhysicianReview"
          component={PhysicianReviewScreen}
          options={{ title: "Revue medecin" }}
        />
        <Stack.Screen
          name="FinalReport"
          component={FinalReportScreen}
          options={{ title: "Rapport final" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
