import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import Animated, { SlideInDown, SlideOutUp } from 'react-native-reanimated';
import { Button } from 'react-native';

export default function WrappedModal({ visible, onClose, data }) {
  if (!visible) return null;

  return (
    <Animated.View
      entering={SlideInDown}
      exiting={SlideOutUp}
      style={styles.modalOverlay}
    >
      <View style={styles.modalContainer}>
        <Text style={styles.modalTitle}>🎉 Your 2024 Wrapped 🎉</Text>
        <ScrollView>
          <Text style={styles.sectionTitle}>✨ Most Visited Locations:</Text>
          {data.mostVisitedLocations.map((location, index) => (
            <Text key={index} style={styles.itemText}>
              🏠 {location.location}: {location.visits} visits
            </Text>
          ))}
          <Text style={styles.sectionTitle}>🍴 Most Purchased Items:</Text>
          {data.mostPurchasedItems.map((item, index) => (
            <Text key={index} style={styles.itemText}>
              🍽️ {item.item}: {item.count} times
            </Text>
          ))}
        </ScrollView>
        <TouchableOpacity style={styles.closeButton} onPress={onClose}>
          <Text style={styles.closeButtonText}>Close</Text>
        </TouchableOpacity>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    position: 'absolute', // Absolute positioning to overlay the entire screen
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)', // Semi-transparent black overlay
    justifyContent: 'center', // Center the modal vertically
    alignItems: 'center', // Center the modal horizontally
    zIndex: 1000, // Ensure it's above other UI elements
  },
  modalContainer: {
    width: '90%',
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 10,
  },
  modalTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2E86C1',
    textAlign: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F618D',
    marginBottom: 10,
    marginTop: 20,
  },
  itemText: {
    fontSize: 16,
    color: '#555',
    marginBottom: 10,
  },
  closeButton: {
    marginTop: 20,
    alignSelf: 'center',
    backgroundColor: '#2E86C1',
    paddingVertical: 10,
    paddingHorizontal: 30,
    borderRadius: 25,
    elevation: 5,
  },
  closeButtonText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',
  },
});