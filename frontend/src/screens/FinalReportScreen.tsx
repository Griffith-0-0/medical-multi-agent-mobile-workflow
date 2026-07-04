import { ScrollView, StyleSheet, Text, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "FinalReport">;

export function FinalReportScreen({ route }: Props) {
  const { consultation } = route.params;
  const answers = consultation.patient_answers ?? [];

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Rapport final</Text>

      <View style={styles.section}>
        <Text style={styles.label}>Cas initial</Text>
        <Text style={styles.body}>{consultation.patient_case}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Reponses patient</Text>
        {answers.map((answer, index) => (
          <View key={`${answer}-${index}`} style={styles.answerRow}>
            <Text style={styles.answerIndex}>{index + 1}</Text>
            <Text style={styles.answerText}>{answer}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Synthese clinique preliminaire</Text>
        <Text style={styles.body}>
          Les informations recueillies permettent une orientation clinique preliminaire. La synthese reste prudente et doit etre interpretee avec la revue du medecin.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Recommandation intermediaire</Text>
        <Text style={styles.body}>{consultation.interim_care}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Revue du medecin</Text>
        <Text style={styles.body}>{consultation.physician_treatment}</Text>
      </View>

      <View style={styles.warningBox}>
        <Text style={styles.warningLabel}>Avertissement</Text>
        <Text style={styles.warningText}>Ce systeme ne remplace pas une consultation medicale.</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 24,
    backgroundColor: "#f8fafc",
    gap: 16,
  },
  title: {
    color: "#0f172a",
    fontSize: 26,
    fontWeight: "800",
    lineHeight: 32,
  },
  section: {
    borderWidth: 1,
    borderColor: "#e2e8f0",
    borderRadius: 8,
    backgroundColor: "#ffffff",
    padding: 14,
    gap: 8,
  },
  label: {
    color: "#334155",
    fontSize: 16,
    fontWeight: "800",
  },
  body: {
    color: "#475569",
    fontSize: 15,
    lineHeight: 22,
  },
  answerRow: {
    flexDirection: "row",
    gap: 10,
    alignItems: "flex-start",
  },
  answerIndex: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    fontSize: 13,
    fontWeight: "800",
    lineHeight: 24,
    textAlign: "center",
  },
  answerText: {
    flex: 1,
    color: "#475569",
    fontSize: 15,
    lineHeight: 22,
  },
  warningBox: {
    borderWidth: 1,
    borderColor: "#bfdbfe",
    borderRadius: 8,
    backgroundColor: "#eff6ff",
    padding: 14,
    gap: 6,
  },
  warningLabel: {
    color: "#1d4ed8",
    fontSize: 16,
    fontWeight: "800",
  },
  warningText: {
    color: "#1e3a8a",
    fontSize: 15,
    lineHeight: 22,
  },
});
