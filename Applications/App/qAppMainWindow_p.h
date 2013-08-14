/*==============================================================================

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAppMainWindow_p_h
#define __qAppMainWindow_p_h

// SlicerApp includes
#include "qAppMainWindow.h"
#include "qSlicerAppMainWindow_p.h"

//-----------------------------------------------------------------------------
class Q_SLICER_APP_EXPORT qAppMainWindowPrivate
  : public qSlicerAppMainWindowPrivate
{
  Q_DECLARE_PUBLIC(qAppMainWindow);
public:
  typedef qSlicerAppMainWindowPrivate Superclass;
  qAppMainWindowPrivate(qAppMainWindow& object);
  virtual ~qAppMainWindowPrivate();

  virtual void init();
  /// Reimplemented for custom behavior
  virtual void setupUi(QMainWindow * mainWindow);
};

#endif
