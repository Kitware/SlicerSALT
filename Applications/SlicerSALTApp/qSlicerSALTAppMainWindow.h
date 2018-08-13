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

#ifndef __qSlicerSALTAppMainWindow_h
#define __qSlicerSALTAppMainWindow_h

// SlicerSALT includes
#include "qSlicerSALTAppExport.h"
class qSlicerSALTAppMainWindowPrivate;

// Slicer includes
#include "qSlicerMainWindow.h"

class Q_SLICERSALT_APP_EXPORT qSlicerSALTAppMainWindow : public qSlicerMainWindow
{
  Q_OBJECT
public:
  typedef qSlicerMainWindow Superclass;

  qSlicerSALTAppMainWindow(QWidget *parent=0);
  virtual ~qSlicerSALTAppMainWindow();

public:
  virtual void show();

public slots:
  void on_HelpAboutSlicerSALTAppAction_triggered();

protected:
  qSlicerSALTAppMainWindow(qSlicerSALTAppMainWindowPrivate* pimpl, QWidget* parent);

private:
  Q_DECLARE_PRIVATE(qSlicerSALTAppMainWindow);
  Q_DISABLE_COPY(qSlicerSALTAppMainWindow);
};

#endif
