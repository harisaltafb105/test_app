'use client'

import React, { createContext, useContext, useReducer, type ReactNode } from 'react'
import type { AppState, TaskAction, FilterType } from '@/types/task'
import { mockedTasks } from '@/lib/mock-data'

// Initial state
const initialState: AppState = {
  tasks: mockedTasks,
  ui: {
    activeFilter: 'all',
    modalOpen: false,
    modalMode: null,
    editingTaskId: null,
    isLoading: false,
    error: null,
  },
}

// Task reducer with all actions
function taskReducer(state: AppState, action: TaskAction): AppState {
  switch (action.type) {
    case 'ADD_TASK': {
      const newTask = {
        ...action.payload,
        id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        createdAt: new Date(),
      }
      return {
        ...state,
        tasks: [...state.tasks, newTask],
      }
    }

    case 'UPDATE_TASK': {
      return {
        ...state,
        tasks: state.tasks.map((task) =>
          task.id === action.payload.id
            ? { ...task, ...action.payload.updates, updatedAt: new Date() }
            : task
        ),
      }
    }

    case 'DELETE_TASK': {
      return {
        ...state,
        tasks: state.tasks.filter((task) => task.id !== action.payload),
      }
    }

    case 'TOGGLE_COMPLETE': {
      return {
        ...state,
        tasks: state.tasks.map((task) =>
          task.id === action.payload ? { ...task, completed: !task.completed } : task
        ),
      }
    }

    case 'SET_FILTER': {
      return {
        ...state,
        ui: { ...state.ui, activeFilter: action.payload },
      }
    }

    case 'OPEN_MODAL': {
      return {
        ...state,
        ui: {
          ...state.ui,
          modalOpen: true,
          modalMode: action.payload.mode,
          editingTaskId: action.payload.taskId || null,
        },
      }
    }

    case 'CLOSE_MODAL': {
      return {
        ...state,
        ui: {
          ...state.ui,
          modalOpen: false,
          modalMode: null,
          editingTaskId: null,
        },
      }
    }

    case 'SET_LOADING': {
      return {
        ...state,
        ui: { ...state.ui, isLoading: action.payload },
      }
    }

    case 'SET_ERROR': {
      return {
        ...state,
        ui: { ...state.ui, error: action.payload },
      }
    }

    default:
      return state
  }
}

// Context type
interface TaskContextType {
  state: AppState
  dispatch: React.Dispatch<TaskAction>
}

// Create context
const TaskContext = createContext<TaskContextType | undefined>(undefined)

// Provider component
export function TaskProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(taskReducer, initialState)

  return (
    <TaskContext.Provider value={{ state, dispatch }}>
      {children}
    </TaskContext.Provider>
  )
}

// Hook to access state
export function useTasks() {
  const context = useContext(TaskContext)
  if (!context) {
    throw new Error('useTasks must be used within TaskProvider')
  }
  return context.state
}

// Hook to access actions
export function useTaskActions() {
  const context = useContext(TaskContext)
  if (!context) {
    throw new Error('useTaskActions must be used within TaskProvider')
  }
  return context.dispatch
}
