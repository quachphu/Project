import { Tabs } from 'expo-router';
import React from 'react';
import { Platform } from 'react-native';
import Ionicons from '@expo/vector-icons/Ionicons';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import Octicons from '@expo/vector-icons/Octicons';


import { HapticTab } from '@/components/HapticTab';
import TabBarBackground from '@/components/ui/TabBarBackground';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarBackground: TabBarBackground,
        tabBarStyle: Platform.select({
          ios: {
            // Use a transparent background on iOS to show the blur effect
            position: 'absolute',
          },
          default: {},
        }),
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: () => <Ionicons name="home" size={22} color="#fff" />
          ,
        }}
      />
      <Tabs.Screen
      name="chat"
      options={{
        title: 'Chat',
        tabBarIcon: () => <Octicons name="light-bulb" size={22} color="white" />,
      }}
    />
      <Tabs.Screen
        name="account"
        options={{
          title: 'Account',
          tabBarIcon: () =>  <MaterialIcons name="account-circle" size={22} color="white" />,
        }}
      />
    </Tabs>
  );
}
