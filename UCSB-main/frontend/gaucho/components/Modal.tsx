import React, { useState } from 'react';
import { Modal, View, Text, StyleSheet, TouchableOpacity, FlatList, Image, ScrollView } from 'react-native';
import { BarChart } from 'react-native-chart-kit';

export default function CustomModal({ visible, onClose, waitTime, menuItems }) {
  const [selectedDay, setSelectedDay] = useState('Monday'); // Default day for bar chart
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const averageTimes = {
    Monday: {
      '8 AM': 10,
      '9 AM': 15,
      '10 AM': 20,
      '11 AM': 18,
      '12 PM': 25,
      '1 PM': 30,
      '2 PM': 28,
      '3 PM': 22,
      '4 PM': 19,
      '5 PM': 26,
    },
    Tuesday: {
      '8 AM': 12,
      '9 AM': 17,
      '10 AM': 23,
      '11 AM': 20,
      '12 PM': 28,
      '1 PM': 35,
      '2 PM': 30,
      '3 PM': 25,
      '4 PM': 21,
      '5 PM': 29,
    },
    Wednesday: {
      '8 AM': 11,
      '9 AM': 16,
      '10 AM': 21,
      '11 AM': 19,
      '12 PM': 27,
      '1 PM': 33,
      '2 PM': 29,
      '3 PM': 24,
      '4 PM': 20,
      '5 PM': 28,
    },
    Thursday: {
      '8 AM': 9,
      '9 AM': 14,
      '10 AM': 19,
      '11 AM': 17,
      '12 PM': 24,
      '1 PM': 32,
      '2 PM': 27,
      '3 PM': 21,
      '4 PM': 18,
      '5 PM': 25,
    },
    Friday: {
      '8 AM': 13,
      '9 AM': 18,
      '10 AM': 25,
      '11 AM': 22,
      '12 PM': 30,
      '1 PM': 38,
      '2 PM': 34,
      '3 PM': 28,
      '4 PM': 23,
      '5 PM': 31,
    },
  };

  const getWaitTimeColor = (waitTime) => {
    if (waitTime <= 10) return 'green';
    if (waitTime <= 20) return 'orange';
    return 'red';
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.modalContainer}>
          <Text style={styles.headerText}>Wait Time 'location'</Text>
          <Text style={[styles.waitTimeText, { color: getWaitTimeColor(waitTime) }]}>
            Current Wait Time: {waitTime} minutes
          </Text>

          <Text style={styles.sectionTitle}>Menu Items</Text>
          {menuItems.length > 0 ? (
            <FlatList
              data={menuItems}
              keyExtractor={(item) => item.id.toString()}
              renderItem={({ item }) => (
                <View style={styles.menuItemContainer}>
                  <Image source={{ uri: item.image }} style={styles.menuItemImage} />
                  <View style={styles.menuItemDetails}>
                    <Text style={styles.menuItemName}>{item.item_name}</Text>
                    <Text style={styles.menuItemPrice}>{item.price}</Text>
                  </View>
                </View>
              )}
              style={styles.menuList}
            />
          ) : (
            <Text style={styles.noItemsText}>No menu items available.</Text>
          )}

          <Text style={styles.sectionTitle}>Average Wait Times</Text>
          <ScrollView horizontal showsVerticalScrollIndicator={false} 
      showsHorizontalScrollIndicator={false}
 style={styles.daySelector}>
            {days.map((day) => (
              <TouchableOpacity
                key={day}
                style={[
                  styles.dayButton,
                  selectedDay === day && styles.selectedDayButton,
                ]}
                onPress={() => setSelectedDay(day)}
              >
                <Text
                  style={[
                    styles.dayButtonText,
                    selectedDay === day && styles.selectedDayButtonText,
                  ]}
                >
                  {day}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <ScrollView horizontal >
          <BarChart
  data={{
    labels: Object.keys(averageTimes[selectedDay]).map((time) => {
      // Convert 24-hour time to 12-hour time with AM/PM
      const [hour, minute] = time.split(':');
      const hourInt = parseInt(hour, 10);
      const isPM = hourInt >= 12;
      const displayHour = hourInt % 12 || 12; // Convert to 12-hour format
      return `${displayHour}${isPM ? ' PM' : ' AM'}`;
    }),
    datasets: [
      {
        data: Object.values(averageTimes[selectedDay]),
      },
    ],
  }}
  width={350} // Adjust based on your layout
  height={200}
  chartConfig={{
    backgroundColor: '#ffffff',
    backgroundGradientFrom: '#ffffff',
    backgroundGradientTo: '#ffffff',
    color: (opacity = 1) => `rgba(34, 128, 176, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
    barPercentage: 0.5,
  }}
  style={styles.barChart}
  yAxisSuffix=" mins" // Add 'mins' suffix to Y-axis labels
  xLabelsOffset={-10} // Adjust position of x-axis labels
  verticalLabelRotation={30} // Rotate labels slightly for better readability
/>
          </ScrollView>

          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Text style={styles.closeButtonText}>Close</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    backgroundColor: '#fff',
    borderRadius: 10,
    width: '90%',
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  headerText: {
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#333',
  },
  waitTimeText: {
    fontSize: 18,
    fontWeight: '500',
    marginBottom: 20,
    textAlign: 'center',
    color: '#555',
  },
  sectionTitle: {
    
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 10,
    color: '#333',
  },
  menuList: {
    maxHeight: 200,
    marginBottom: 20,
  },
  menuItemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    backgroundColor: '#f9f9f9',
    padding: 10,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  menuItemImage: {
    width: 50,
    height: 50,
    borderRadius: 5,
    marginRight: 10,
  },
  menuItemDetails: {
    flex: 1,
  },
  menuItemName: {
    fontSize: 16,
    color: '#444',
  },
  menuItemPrice: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#444',
  },
  noItemsText: {
    fontSize: 16,
    color: '#777',
    textAlign: 'center',
    marginVertical: 20,
  },
  daySelector: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  dayButton: {
    padding: 10,
    backgroundColor: '#ddd',
    marginRight: 5,
    borderRadius: 5,
  },
  selectedDayButton: {
    backgroundColor: '#007BFF',
  },
  dayButtonText: {
    color: '#333',
  },
  selectedDayButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  barChart: {
    marginVertical: 10,
    borderRadius: 10,
  },
  closeButton: {
    backgroundColor: '#007BFF',
    borderRadius: 5,
    paddingVertical: 10,
    paddingHorizontal: 20,
    alignSelf: 'center',
  },
  closeButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
});