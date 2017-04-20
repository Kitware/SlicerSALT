/*==============================================================================

  Copyright (c) Kitware, Inc.

  See http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware, Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

#ifndef __qAppMainWindow_h
#define __qAppMainWindow_h

// Slicer includes
#include "qSlicerAppExport.h"
#include "qSlicerAppMainWindow.h"
class qAppMainWindowPrivate;

class Q_SLICER_APP_EXPORT qAppMainWindow
  : public qSlicerAppMainWindow
{
  Q_OBJECT
public:

  typedef qSlicerAppMainWindow Superclass;
  qAppMainWindow(QWidget *parent=0);
  virtual ~qAppMainWindow();

public:
  /// Reimplemented to use qAppAboutDialog instead of qSlicerAppAboutDialog.
  virtual void on_HelpAboutSlicerAppAction_triggered();
  virtual void show();

private:
  Q_DECLARE_PRIVATE(qAppMainWindow);
  Q_DISABLE_COPY(qAppMainWindow);
};

#endif
